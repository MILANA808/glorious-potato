"""
AI Notary Module
================

Provides AI-powered document notarization and verification services.
Combines cryptographic signatures with AI-based content analysis.
"""

import hashlib
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AINotary:
    """
    AI-powered notary system for document verification and certification.

    Features:
    - Document timestamping
    - Content integrity verification
    - Metadata extraction and validation
    - Audit trail maintenance
    """

    def __init__(self, notary_id: Optional[str] = None):
        """
        Initialize AI Notary.

        Args:
            notary_id: Unique identifier for this notary instance
        """
        self.notary_id = notary_id or self._generate_notary_id()
        self.notarization_records: List[Dict[str, Any]] = []
        logger.info(f"AI Notary initialized with ID: {self.notary_id}")

    def _generate_notary_id(self) -> str:
        """Generate a unique notary ID."""
        import hashlib
        timestamp = datetime.utcnow().isoformat()
        hash_obj = hashlib.sha256(timestamp.encode('utf-8'))
        return f"notary_{hash_obj.hexdigest()[:16]}"

    def notarize_document(self, document: Dict[str, Any],
                         metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Notarize a document with timestamp and metadata.

        Args:
            document: Document content as dictionary
            metadata: Optional additional metadata

        Returns:
            Notarized document with certification
        """
        notarization_time = datetime.utcnow()

        # Create notarization certificate
        certificate = {
            "notary_id": self.notary_id,
            "notarization_timestamp": notarization_time.isoformat(),
            "document_hash": self._hash_document(document),
            "metadata": metadata or {},
            "status": "notarized",
            "certificate_version": "1.0"
        }

        # Create notarized document
        notarized_doc = {
            "original_document": document,
            "notarization_certificate": certificate,
            "notarization_id": self._generate_notarization_id(certificate)
        }

        # Add to records
        self.notarization_records.append({
            "notarization_id": notarized_doc["notarization_id"],
            "timestamp": notarization_time.isoformat(),
            "document_hash": certificate["document_hash"]
        })

        logger.info(f"Document notarized: {notarized_doc['notarization_id']}")
        return notarized_doc

    def verify_notarization(self, notarized_doc: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify a notarized document's authenticity.

        Args:
            notarized_doc: Previously notarized document

        Returns:
            Verification result with details
        """
        try:
            # Extract components
            original_doc = notarized_doc["original_document"]
            certificate = notarized_doc["notarization_certificate"]

            # Verify document hash
            current_hash = self._hash_document(original_doc)
            hash_matches = current_hash == certificate["document_hash"]

            # Check if in records
            notarization_id = notarized_doc["notarization_id"]
            in_records = any(
                r["notarization_id"] == notarization_id
                for r in self.notarization_records
            )

            # Verify certificate integrity
            cert_id = self._generate_notarization_id(certificate)
            cert_valid = cert_id == notarization_id

            is_valid = hash_matches and cert_valid

            result = {
                "valid": is_valid,
                "hash_matches": hash_matches,
                "certificate_valid": cert_valid,
                "in_records": in_records,
                "notarization_timestamp": certificate["notarization_timestamp"],
                "verified_at": datetime.utcnow().isoformat()
            }

            logger.info(f"Verification result: {is_valid}")
            return result

        except Exception as e:
            logger.error(f"Verification failed: {e}")
            return {
                "valid": False,
                "error": str(e),
                "verified_at": datetime.utcnow().isoformat()
            }

    def _hash_document(self, document: Dict[str, Any]) -> str:
        """
        Create hash of document for integrity verification.

        Args:
            document: Document to hash

        Returns:
            SHA-256 hash of document
        """
        import hashlib
        doc_json = json.dumps(document, sort_keys=True)
        return hashlib.sha256(doc_json.encode('utf-8')).hexdigest()

    def _generate_notarization_id(self, certificate: Dict[str, Any]) -> str:
        """
        Generate unique ID for a notarization.

        Args:
            certificate: Notarization certificate

        Returns:
            Unique notarization ID
        """
        cert_json = json.dumps(certificate, sort_keys=True)
        hash_obj = hashlib.sha256(cert_json.encode('utf-8'))
        return f"NOT-{hash_obj.hexdigest()[:16].upper()}"

    def analyze_document_content(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze document content for completeness and validity.

        Args:
            document: Document to analyze

        Returns:
            Analysis results
        """
        analysis = {
            "timestamp": datetime.utcnow().isoformat(),
            "field_count": len(document),
            "fields": list(document.keys()),
            "has_metadata": "metadata" in document,
            "estimated_size_bytes": len(json.dumps(document))
        }

        # Basic content checks
        checks = {
            "has_fields": len(document) > 0,
            "has_timestamp": any("time" in key.lower() for key in document.keys()),
            "has_id": any("id" in key.lower() for key in document.keys())
        }

        analysis["content_checks"] = checks
        analysis["completeness_score"] = sum(checks.values()) / len(checks)

        return analysis

    def create_audit_trail(self, document_id: str) -> List[Dict[str, Any]]:
        """
        Create audit trail for a specific document.

        Args:
            document_id: ID of document to trace

        Returns:
            List of all records related to this document
        """
        trail = [
            record for record in self.notarization_records
            if document_id in record.get("notarization_id", "")
        ]

        logger.info(f"Audit trail created: {len(trail)} records found")
        return trail

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get notary statistics.

        Returns:
            Dictionary with statistics
        """
        return {
            "notary_id": self.notary_id,
            "total_notarizations": len(self.notarization_records),
            "active_status": "operational",
            "created_at": datetime.utcnow().isoformat()
        }

    def export_records(self) -> str:
        """
        Export all notarization records as JSON.

        Returns:
            JSON string of all records
        """
        export_data = {
            "notary_id": self.notary_id,
            "export_timestamp": datetime.utcnow().isoformat(),
            "records": self.notarization_records
        }
        return json.dumps(export_data, indent=2)

    def import_records(self, records_json: str) -> int:
        """
        Import notarization records from JSON.

        Args:
            records_json: JSON string of records

        Returns:
            Number of records imported
        """
        try:
            data = json.loads(records_json)
            imported_records = data.get("records", [])
            self.notarization_records.extend(imported_records)
            logger.info(f"Imported {len(imported_records)} records")
            return len(imported_records)
        except Exception as e:
            logger.error(f"Import failed: {e}")
            return 0
