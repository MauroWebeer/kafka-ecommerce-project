
# User Login Events

This topic stores events related to user login actions.

### Event Schema

- `event_name`: Name of the event (e.g., login).
- `event_id`: Unique identifier for the event.
- `event_type`: Type of the event (e.g., user_action).
- `user_id`: Unique identifier for the user.
- `timestamp`: Timestamp of the login event.

### Example Event:
```json
{
  "event_name": "login",
  "event_id": "67890",
  "event_type": "user_action",
  "user_id": "user123",
  "timestamp": "2025-03-10T12:30:00"
}
