"""Tool functions built on top of integrations for use with Vapi."""

from .calendar import (
    create_calendar_event,
    list_calendar_events,
    get_calendar_event,
    update_calendar_event,
    delete_calendar_event,
    get_free_busy_times
)
from .tasks import *
from .communication import *
from .ai import *
from .storage import upload_file, download_file, list_files

# Note: Import additional tool modules as they are implemented

__all__ = [
    # Calendar tools
    "create_calendar_event",
    "list_calendar_events",
    "get_calendar_event",
    "update_calendar_event",
    "delete_calendar_event",
    "get_free_busy_times",
    
    # Task management tools
    "create_task",
    "list_tasks",
    "complete_task",
    "update_task",
    "delete_task",
    
    # Communication tools
    "send_slack_message",
    "send_text_message",
    
    # AI tools
    "generate_text",
    "generate_chat_response",
    "generate_image",
    
    # Storage tools
    "upload_file",
    "download_file",
    "list_files",
] 