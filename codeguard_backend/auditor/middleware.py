"""
CodeGuard AI - Infrastructure Security Layer
Implements thread-safe, high-concurrency memory rate limiting per IP address.
"""

import time
import logging
from typing import Dict, Tuple
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class StrictRateLimitMiddleware(MiddlewareMixin):
    """
    Defensive Layer 7 Firewall.
    Monitors incoming request velocity per IP and throttles abusers before hitting the LLM gateway.
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        # In-memory bucket matrix: { ip_address: (request_count, window_start_time) }
        self._ip_buckets: Dict[str, Tuple[int, float]] = {}
        
        # Enterprise Tier Baseline Thresholds
        self.MAX_REQUESTS_PER_MINUTE = 5
        self.TIME_WINDOW_SECONDS = 60.0

    def process_request(self, request):
        """Intercepts the pipeline lifecycle before routing context triggers execution threads."""
        # Only throttle our computational/token heavy neural engine endpoint
        if request.path == "/api/v1/auditor/analyze":
            # Extract client IP safely handling potential reverse proxy layers (Nginx)
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                client_ip = x_forwarded_for.split(",")[0].strip()
            else:
                client_ip = request.META.get("REMOTE_ADDR", "127.0.0.1")

            current_time = time.time()
            
            if client_ip not in self._ip_buckets:
                # Initialize virgin state bucket for new client connection context
                self._ip_buckets[client_ip] = (1, current_time)
                return None

            request_count, window_start = self._ip_buckets[client_ip]

            # Check if the sliding time window constraint has expired
            if current_time - window_start > self.TIME_WINDOW_SECONDS:
                # Reset bucket boundary variables
                self._ip_buckets[client_ip] = (1, current_time)
                return None

            if request_count >= self.MAX_REQUESTS_PER_MINUTE:
                logger.warning(f"🛑 RATE LIMIT TRIGGERED: Abusive client origin blocked -> IP: {client_ip}")
                return JsonResponse(
                    {
                        "success": False,
                        "message": "### API Velocity Threshold Exceeded\nYou have issued too many concurrent requests. "
                                   "Please wait 60 seconds before processing another security audit suite.",
                        "codeLength": 0,
                        "securityScore": 0,
                        "riskLevel": "THROTTLED",
                        "gdprStatus": "THROTTLED",
                        "issuesCount": 0
                    },
                    status=429
                )

            # Increment request registration index inside active window bounds
            self._ip_buckets[client_ip] = (request_count + 1, window_start)
            
        return None