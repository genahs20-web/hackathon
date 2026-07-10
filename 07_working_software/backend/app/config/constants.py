"""Constants shared across the backend, mirroring deliverables/06_specs/validation_rules.yaml."""

MAX_FILE_SIZE_BYTES = 52_428_800  # 50MB
MAX_DOCUMENTS_PER_USER = 100
MAX_QUERY_LENGTH = 2000
MAX_TAGS_PER_DOCUMENT = 10

ALLOWED_FILE_EXTENSIONS = {".pdf", ".docx", ".pptx", ".xlsx", ".eml"}

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "message/rfc822",
}

CHUNK_SIZE_TOKENS = 500
CHUNK_OVERLAP_TOKENS = 50

RETRIEVAL_TOP_K = 5
RETRIEVAL_SIMILARITY_FLOOR = 0.5

CONFLICT_MIN_DOCUMENTS = 3
CONFLICT_CONFIDENCE_THRESHOLD = 0.6

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

PROMPT_INJECTION_PATTERNS = [
    r"<script.*?</script>",
    r"(?i)DROP\s+TABLE",
    r"(?i)DELETE\s+FROM",
    r"(?i)ignore (all )?(previous|prior|above) instructions",
    r"(?i)system prompt",
]
