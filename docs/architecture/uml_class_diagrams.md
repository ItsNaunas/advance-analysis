# UML Class Diagrams

## Domain Models

```
┌─────────────────────────────────────────────────────────┐
│                        User                             │
├─────────────────────────────────────────────────────────┤
│ - id: Integer                                           │
│ - username: String                                       │
│ - email: String                                          │
│ - password_hash: String                                  │
│ - role: String                                          │
│ - created_at: DateTime                                   │
│ - last_login: DateTime                                  │
│ - failed_login_attempts: Integer                         │
│ - locked_until: DateTime                                │
├─────────────────────────────────────────────────────────┤
│ + is_locked(): Boolean                                  │
│ + has_role(role): Boolean                               │
│ + is_head_chef(): Boolean                               │
│ + is_admin(): Boolean                                   │
│ + can_manage_users(): Boolean                           │
│ + can_view_reports(): Boolean                           │
└─────────────────────────────────────────────────────────┘
                          │
                          │ 1
                          │
                          │ *
┌─────────────────────────────────────────────────────────┐
│                      Inventory                           │
├─────────────────────────────────────────────────────────┤
│ - id: Integer                                           │
│ - item_name: String                                      │
│ - quantity: Integer                                      │
│ - supplier_id: Integer                                   │
│ - date_added: Date                                      │
│ - expiration_date: Date                                  │
│ - created_by: Integer                                    │
│ - created_at: DateTime                                   │
├─────────────────────────────────────────────────────────┤
│ + is_expiring_soon(days): Boolean                       │
│ + is_expired(): Boolean                                 │
│ + is_low_stock(): Boolean                               │
│ + to_dict(): Dictionary                                 │
└─────────────────────────────────────────────────────────┘
                          │
                          │ *
                          │
                          │ 1
┌─────────────────────────────────────────────────────────┐
│                      Supplier                            │
├─────────────────────────────────────────────────────────┤
│ - id: Integer                                           │
│ - name: String                                          │
│ - contact_info: Text                                     │
│ - created_at: DateTime                                   │
├─────────────────────────────────────────────────────────┤
│ + to_dict(): Dictionary                                 │
└─────────────────────────────────────────────────────────┘
```

## Service Layer

```
┌─────────────────────────────────────────────────────────┐
│                    AuthService                           │
├─────────────────────────────────────────────────────────┤
│ - user_repo: UserRepository                             │
├─────────────────────────────────────────────────────────┤
│ + authenticate(username, password): (User, Error)       │
│ + create_user(...): (User, Error)                       │
│ + change_password(...): (Boolean, Error)                │
└─────────────────────────────────────────────────────────┘
                          │
                          │ uses
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  UserRepository                          │
├─────────────────────────────────────────────────────────┤
│ + get_by_id(id): User                                   │
│ + get_by_username(username): User                       │
│ + create(...): User                                     │
│ + update(user): User                                    │
│ + delete(user): void                                    │
│ + increment_failed_login(user): User                     │
│ + reset_failed_login(user): User                        │
└─────────────────────────────────────────────────────────┘
                          │
                          │ uses
                          ▼
┌─────────────────────────────────────────────────────────┐
│                        User                              │
└─────────────────────────────────────────────────────────┘
```

## Controller Layer

```
┌─────────────────────────────────────────────────────────┐
│                  InventoryController                     │
├─────────────────────────────────────────────────────────┤
│ - inventory_service: InventoryService                    │
├─────────────────────────────────────────────────────────┤
│ + list(): Response                                      │
│ + add(): Response                                       │
│ + remove(item_id): Response                             │
│ + api_list(): JSON                                      │
│ + api_add(): JSON                                       │
└─────────────────────────────────────────────────────────┘
                          │
                          │ uses
                          ▼
┌─────────────────────────────────────────────────────────┐
│                 InventoryService                         │
├─────────────────────────────────────────────────────────┤
│ - inventory_repo: InventoryRepository                    │
│ - audit_repo: AuditRepository                           │
├─────────────────────────────────────────────────────────┤
│ + add_item(...): (Item, Error)                          │
│ + remove_item(...): (Item, Error)                       │
│ + update_item(...): (Item, Error)                        │
│ + get_all_items(): List[Item]                           │
│ + get_expiring_soon(days): List[Item]                   │
│ + get_low_stock(): List[Item]                           │
└─────────────────────────────────────────────────────────┘
                          │
                          │ uses
                          ▼
┌─────────────────────────────────────────────────────────┐
│              InventoryRepository                         │
├─────────────────────────────────────────────────────────┤
│ + get_by_id(id): Inventory                              │
│ + get_all(): List[Inventory]                            │
│ + create(...): Inventory                                 │
│ + update(item): Inventory                                │
│ + delete(item): void                                     │
│ + find_duplicate(...): Inventory                         │
└─────────────────────────────────────────────────────────┘
```

## Middleware

```
┌─────────────────────────────────────────────────────────┐
│              RBACMiddleware                              │
├─────────────────────────────────────────────────────────┤
│ + require_role(*roles): Decorator                        │
│ + require_authenticated: Decorator                       │
│ + require_head_chef_or_admin: Decorator                 │
│ + require_admin: Decorator                               │
└─────────────────────────────────────────────────────────┘
```

## Relationships Summary

- **User** has many **Inventory** items (created_by)
- **User** has many **Deliveries** (delivery_person_id)
- **User** has many **Notifications**
- **User** has many **AuditLogs**
- **Supplier** has many **Inventory** items
- **Inventory** belongs to one **Supplier** (optional)
- **Inventory** belongs to one **User** (creator)
- **Delivery** belongs to one **User** (delivery_person)
- **Notification** belongs to one **User**
- **Reorder** belongs to one **User** (confirmed_by)
