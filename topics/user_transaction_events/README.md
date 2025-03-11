
# User Transaction Events

This topic stores events related to user transactions, such as purchases.

### Event Schema

- `event_name`: Name of the event (e.g., purchase).
- `event_id`: Unique identifier for the event.
- `event_type`: Type of the event (e.g., transaction).
- `user_id`: Unique identifier for the user making the transaction.
- `transaction_amount`: Amount of the transaction.
- `timestamp`: Timestamp of the transaction.

### Example Event:
```json
{
  "event_name": "purchase",
  "event_id": "98765",
  "event_type": "transaction",
  "user_id": "user123",
  "transaction_amount": 100.50,
  "timestamp": "2025-03-10T12:45:00"
}
