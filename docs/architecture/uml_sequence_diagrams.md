# UML Sequence Diagrams

## User Authentication Flow

```
User          Browser         AuthController    AuthService    UserRepository    Database
  │              │                  │                │              │              │
  │──Login──────>│                  │                │              │              │
  │              │──POST /login───>│                │              │              │
  │              │                  │──authenticate──>│              │              │
  │              │                  │                │──get_by_username──>│              │
  │              │                  │                │              │──SELECT─────>│
  │              │                  │                │              │<──User───────│
  │              │                  │                │──verify_password│              │
  │              │                  │                │              │              │
  │              │                  │                │<──User───────│              │
  │              │                  │<──User────────│              │              │
  │              │<──Session───────│                │              │              │
  │<──Redirect───│                  │                │              │              │
  │              │                  │                │              │              │
```

## Add Inventory Item Flow

```
User          Browser    InventoryController  InventoryService  InventoryRepository  AuditRepository  Database
  │              │              │                    │                  │                  │              │
  │──Add Item───>│              │                    │                  │                  │              │
  │              │──POST /inventory/add──>│                    │                  │                  │              │
  │              │              │──add_item──────────>│                  │                  │              │
  │              │              │                    │──find_duplicate──>│                  │              │
  │              │              │                    │                  │──SELECT───────>│              │
  │              │              │                    │                  │<──Result───────│              │
  │              │              │                    │──create──────────>│                  │              │
  │              │              │                    │                  │──INSERT───────>│              │
  │              │              │                    │                  │<──Item─────────│              │
  │              │              │                    │──log_action──────>│                  │              │
  │              │              │                    │                  │                  │──INSERT─────>│
  │              │              │<──Item─────────────│                  │                  │              │
  │              │<──Success───│                    │                  │                  │              │
  │<──Redirect───│              │                    │                  │                  │              │
  │              │              │                    │                  │                  │              │
```

## Generate Reorder Flow

```
Scheduler    ReorderService  InventoryService  InventoryRepository  NotificationService  UserRepository  Database
  │                │                │                  │                      │                  │              │
  │──Monday───────>│                │                  │                      │                  │              │
  │                │──generate_reorder_list           │                  │                      │                  │              │
  │                │                │──get_low_stock──>│                  │                      │                  │              │
  │                │                │                  │──SELECT───────────>│                      │                  │              │
  │                │                │                  │<──Items────────────│                      │                  │              │
  │                │                │──get_expiring_soon>│                  │                      │                  │              │
  │                │                │                  │──SELECT───────────>│                      │                  │              │
  │                │                │                  │<──Items────────────│                      │                  │              │
  │                │                │<──Items──────────│                  │                      │                  │              │
  │                │──create_reorder│                  │                  │                      │                  │              │
  │                │                │                  │                  │                      │                  │──INSERT─────>│
  │                │                │                  │                  │──create_notification>│                  │              │
  │                │                │                  │                  │                      │──get_by_role───>│              │
  │                │                │                  │                  │                      │                  │──SELECT─────>│
  │                │                │                  │                  │                      │<──HeadChefs─────│              │
  │                │                │                  │                  │──INSERT──────────────>│                  │              │
  │                │                │                  │                  │                      │                  │──INSERT─────>│
  │                │<──Reorder──────│                  │                  │                      │                  │              │
  │                │                │                  │                  │                      │                  │              │
```

## Delivery Confirmation Flow

```
DeliveryPerson  Browser    DeliveryController  DeliveryService  AuditRepository  Database
      │            │              │                  │                  │              │
      │──Confirm──>│              │                  │                  │              │
      │            │──POST /deliveries/:id/confirm>│                  │                  │              │
      │            │              │──confirm_delivery>│                  │                  │              │
      │            │              │                  │──get_by_id───────>│                  │              │
      │            │              │                  │                  │──SELECT───────>│              │
      │            │              │                  │                  │<──Delivery─────│              │
      │            │              │                  │──update_status───>│                  │              │
      │            │              │                  │                  │──UPDATE───────>│              │
      │            │              │                  │                  │<──Updated──────│              │
      │            │              │──log_action──────>│                  │              │
      │            │              │                  │                  │──INSERT───────>│              │
      │            │<──Success────│                  │                  │                  │              │
      │<──Redirect─│              │                  │                  │                  │              │
      │            │              │                  │                  │                  │              │
```

## Notification Check Flow

```
BackgroundTask  NotificationService  InventoryService  InventoryRepository  UserRepository  Database
      │                │                    │                  │                  │              │
      │──Hourly───────>│                    │                  │                  │              │
      │                │──check_expiry_warnings│                  │                  │              │
      │                │                    │──get_expiring_soon>│                  │              │
      │                │                    │                  │──SELECT─────────>│              │
      │                │                    │                  │<──Items──────────│              │
      │                │                    │<──Items──────────│                  │              │
      │                │──get_head_chefs───>│                  │                  │              │
      │                │                    │                  │                  │──SELECT─────>│
      │                │                    │                  │                  │<──HeadChefs──│
      │                │──create_notifications│                  │                  │              │
      │                │                    │                  │                  │──INSERT─────>│
      │                │                    │                  │                  │              │
      │                │                    │                  │                  │              │
```
