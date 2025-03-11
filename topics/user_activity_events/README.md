# User Activity Events

This topic is used to store user activity events. These events represent various actions that users take while interacting with the system.

### Event Schema

- `event_name`: Name of the event (e.g., page_view, click).
- `event_id`: Unique identifier for the event.
- `event_type`: Type of the event (e.g., user_action, system_event).
- `path`: URL or path related to the event.
- `event_properties`: Additional properties related to the event, such as `user_id` and `timestamp`.

### Example Event:
```json
{
  "event_name": "page_view",
  "event_id": "12345",
  "event_type": "user_action",
  "path": "/home",
  "event_properties": {
    "user_id": "user123",
    "timestamp": "2025-03-10T12:00:00"
  }
}
