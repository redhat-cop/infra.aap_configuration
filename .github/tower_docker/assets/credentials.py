DATABASES = {
    'default': {
        'ATOMIC_REQUESTS': True,
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "awx",
        'USER': "awx",
        'PASSWORD': "awxpass",
        'HOST': "postgres",
        'PORT': "5432",
    }
}

BROADCAST_WEBSOCKET_SECRET = "TnREdGRNV2Jqb0hEMzY5LXBjV3Y3NElNX19ta2dGQy1HdVkzS3FobXprY0lqMXl2QzNwN0JQeW1QalVnd2lmSTlzUWtqeEssSnUuUHZUazNkN3pEcmNVa2hRR0pWQXQ0THJpYmpHQVkxRmtnLnVmLVVnay1DMnlqXywwUGdtMkk="
