import os

AION_API_KEY = 'AION_API_KEY'
INVALID_API_KEY = 'INVALID_API_KEY'
AION_BASE_URL = 'https://api.aionlabs.ai/v1'

NO_SUBJECT_TOKEN = 'NO_SUBJECT'
RANDOM_SUBJECT = 'A random positive and motivational topic'
RANDOM_SUBJECT_LIST = [
    "LOVE",
    "COURAGE",
    "HAPPINESS",
    "SADNESS",
    "ANGER",
    "HOPE",
    "LONELINESS",
    "NOSTALGIA",
    "GRATITUDE",
    "FEAR",
    "HEARTBREAK",
    "PEACE",
    "ANXIETY",
    "JOY",
    "REGRET",
    "RESILIENCE",
    "PERSEVERANCE",
    "DISCIPLINE",
    "CONFIDENCE",
    "SELF-LOVE",
    "SELF-RESPECT",
    "PATIENCE",
    "DETERMINATION",
    "AMBITION",
    "MOTIVATION",
    "PERSONAL GROWTH",
    "INDEPENDENCE",
    "BRAVERY",
    "SELF-DISCOVERY",
    "INNER STRENGTH",
    "FRIENDSHIP",
    "LOYALTY",
    "TRUST",
    "BETRAYAL",
    "FORGIVENESS",
    "SOULMATES",
    "FAMILY",
    "COMPASSION",
    "SACRIFICE",
    "LETTING GO",
    "LIFE",
    "DEATH",
    "TIME",
    "FATE",
    "DESTINY",
    "PURPOSE",
    "CHANGE",
    "UNCERTAINTY",
    "SECOND CHANCES",
    "NEW BEGINNINGS",
    "WISDOM",
    "TRUTH",
    "KNOWLEDGE",
    "JUSTICE",
    "FREEDOM",
    "FREE WILL",
    "HUMAN NATURE",
    "STOICISM",
    "EXISTENTIALISM",
    "MORALITY",
    "SUCCESS",
    "FAILURE",
    "HARD WORK",
    "ACHIEVEMENT",
    "DREAMS",
    "LEADERSHIP",
    "CREATIVITY",
    "FOCUS",
    "EXCELLENCE",
    "LEGACY",
    "DARKNESS",
    "REVENGE",
    "OBSESSION",
    "MADNESS",
    "CHAOS",
    "CORRUPTION",
    "GREED",
    "ENVY",
    "SUFFERING",
    "MORAL AMBIGUITY",
    "SPIRITUALITY",
    "FAITH",
    "MINDFULNESS",
    "ACCEPTANCE",
    "ENLIGHTENMENT",
    "KARMA",
    "HUMILITY",
    "INNER PEACE",
    "BALANCE",
    "HUMANITY",
    "SOCIETY",
    "WAR",
    "INEQUALITY",
    "POWER",
    "OPPRESSION",
    "REVOLUTION",
    "HYPOCRISY",
    "NATURE",
    "THE UNIVERSE"
]

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
RABBITMQ_QUEUE_TYPE = os.getenv(
    "RABBITMQ_QUEUE_TYPE",
    "quorum"
)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_JOB_ID_PREFIX = 'quote_job:'
REDIS_URL = os.getenv("REDIS_URL")
