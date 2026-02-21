import pandas as pd
from sqlalchemy import text
from typing import Dict, Any
from backend.connectors.postgres import PostgresConnector

class QualityService:
    def __init__(self, connector: PostgresConnector):
        self.connector = connector

    def get_table_quality(self, table_name: str) -> Dict[str, Any]:
        with self.connector.engine.connect() as conn:
            # 1. Basic counts
            count_res = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
            if count_res == 0:
                return {"error": "Table is empty"}

            metrics = {
                "row_count": count_res,
                "columns": {}
            }

            # 2. Get column list
            columns = conn.execute(text(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'")).fetchall()
            
            total_score = 0
            num_cols = len(columns)

            for col_name, data_type in columns:
                # Optimized SQL for metrics
                sq_query = text(f"""
                    SELECT 
                        COUNT({col_name}) as non_null_count,
                        COUNT(DISTINCT {col_name}) as distinct_count,
                        (COUNT(*) - COUNT({col_name})) as null_count
                    FROM {table_name}
                """)
                res = conn.execute(sq_query).fetchone()
                
                non_null = res.non_null_count
                distinct = res.distinct_count
                null_count = res.null_count
                
                null_percentage = (null_count / count_res) * 100
                distinct_ratio = distinct / count_res
                
                # Uniqueness estimate (duplicate count / total)
                # Note: Exact duplicates are hard in pure SQL without GROUP BY everything, 
                # but we can estimate based on row_count - distinct_count for single column
                duplicate_percentage = ((count_res - distinct) / count_res) * 100

                col_metrics = {
                    "null_percentage": round(null_percentage, 2),
                    "distinct_ratio": round(distinct_ratio, 4),
                    "duplicate_percentage": round(duplicate_percentage, 2),
                }

                # Statistical metrics for numeric
                if data_type in ('integer', 'numeric', 'real', 'double precision', 'bigint', 'smallint'):
                    stat_res = conn.execute(text(f"SELECT MIN({col_name}), MAX({col_name}), AVG({col_name}), STDDEV({col_name}) FROM {table_name}")).fetchone()
                    col_metrics.update({
                        "min": float(stat_res[0]) if stat_res[0] is not None else None,
                        "max": float(stat_res[1]) if stat_res[1] is not None else None,
                        "mean": float(stat_res[2]) if stat_res[2] is not None else None,
                        "std": float(stat_res[3]) if stat_res[3] is not None else None
                    })

                metrics["columns"][col_name] = col_metrics
                total_score += (100 - null_percentage)

            metrics["health_score"] = round(total_score / num_cols, 2) if num_cols > 0 else 0
            return metrics

