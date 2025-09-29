# app/cache/metrics.py
from .redis_config import cache_manager
import time

class CacheMetrics:

    @staticmethod
    def track_cache_hit(key: str):
        """Registra un hit de cache para Clínica Estética"""
        metric_key = f"beauty_metrics:cache_hits:{int(time.time() // 300)}"  # 5 min buckets
        cache_manager.redis_client.incr(metric_key)
        cache_manager.redis_client.expire(metric_key, 3600)  # Expira en 1 hora

    @staticmethod
    def track_cache_miss(key: str):
        """Registra un miss de cache para Clínica Estética"""
        metric_key = f"beauty_metrics:cache_misses:{int(time.time() // 300)}"
        cache_manager.redis_client.incr(metric_key)
        cache_manager.redis_client.expire(metric_key, 3600)

    @staticmethod
    def get_cache_stats():
        """Obtiene estadísticas de cache de Redis relevantes para Clínica Estética"""
        info = cache_manager.redis_client.info()
        return {
            'connected_clients': info.get('connected_clients', 0),
            'used_memory': info.get('used_memory_human', '0B'),
            'keyspace_hits': info.get('keyspace_hits', 0),
            'keyspace_misses': info.get('keyspace_misses', 0),
            'hit_rate_percentage': (info.get('keyspace_hits', 0) / (info.get('keyspace_hits', 0) + info.get('keyspace_misses', 1))) * 100 if (info.get('keyspace_hits', 0) + info.get('keyspace_misses', 1)) > 0 else 0
        }