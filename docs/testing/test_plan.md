# FFSmart Test Plan

## Test Strategy

The testing strategy for FFSmart follows a comprehensive approach covering unit tests, integration tests, and performance tests.

## Test Types

### 1. Unit Tests

**Purpose**: Test individual components in isolation

**Coverage**:
- Services (AuthService, InventoryService, NotificationService, ReorderService)
- Repositories (UserRepository, InventoryRepository, AuditRepository)
- Utilities (password_hasher, validators)
- Models (business logic methods)

**Tools**: pytest

**Location**: `tests/unit/`

### 2. Integration Tests

**Purpose**: Test interactions between components

**Coverage**:
- API endpoints
- Authentication flows
- Database operations
- RBAC enforcement
- End-to-end user workflows

**Tools**: pytest with Flask test client

**Location**: `tests/integration/`

### 3. Performance Tests

**Purpose**: Verify system meets performance requirements

**Coverage**:
- Response times (< 2s for add/remove, < 1s for queries)
- Concurrent user handling (20 users)
- Database performance with 10,000+ records
- Notification delivery time (< 5 seconds)

**Tools**: pytest with performance profiling

## Test Cases

### Authentication Tests

#### TC-AUTH-001: Successful Login
- **Precondition**: Valid user exists
- **Steps**: Submit login form with correct credentials
- **Expected**: User logged in, redirected to dashboard

#### TC-AUTH-002: Failed Login - Invalid Password
- **Precondition**: Valid user exists
- **Steps**: Submit login form with incorrect password
- **Expected**: Error message displayed, failed attempt logged

#### TC-AUTH-003: Account Lockout
- **Precondition**: Valid user exists
- **Steps**: Attempt login 3 times with wrong password
- **Expected**: Account locked, appropriate message displayed

#### TC-AUTH-004: Logout
- **Precondition**: User is logged in
- **Steps**: Click logout button
- **Expected**: User logged out, redirected to login page

### Inventory Tests

#### TC-INV-001: Add Item
- **Precondition**: User logged in with inventory access
- **Steps**: Fill add item form, submit
- **Expected**: Item added to inventory, success message

#### TC-INV-002: Add Duplicate Item
- **Precondition**: Item exists with same name, supplier, expiration
- **Steps**: Add item with same details
- **Expected**: Quantity added to existing item, not new entry

#### TC-INV-003: Remove Item
- **Precondition**: Item exists with quantity > 0
- **Steps**: Remove quantity
- **Expected**: Quantity decreased, audit log created

#### TC-INV-004: Remove More Than Available
- **Precondition**: Item exists with quantity = 5
- **Steps**: Attempt to remove 10
- **Expected**: Error message, quantity unchanged

### Notification Tests

#### TC-NOT-001: Expiry Warning Generation
- **Precondition**: Item expiring within 3 days exists
- **Steps**: Run notification check
- **Expected**: Notification created for Head Chef

#### TC-NOT-002: Low Stock Warning
- **Precondition**: Item with quantity <= 5 exists
- **Steps**: Run notification check
- **Expected**: Notification created for Head Chef

#### TC-NOT-003: Mark Notification as Read
- **Precondition**: Unread notification exists
- **Steps**: Click "Mark as Read"
- **Expected**: Notification marked as read

### Reorder Tests

#### TC-REO-001: Generate Reorder
- **Precondition**: Low stock or expiring items exist
- **Steps**: Trigger reorder generation
- **Expected**: Reorder list created with items

#### TC-REO-002: Confirm Reorder
- **Precondition**: Pending reorder exists, Head Chef logged in
- **Steps**: Click "Confirm Reorder"
- **Expected**: Reorder status changed to CONFIRMED

#### TC-REO-003: Cancel Reorder
- **Precondition**: Pending reorder exists, Head Chef logged in
- **Steps**: Click "Cancel Reorder"
- **Expected**: Reorder status changed to CANCELLED

### RBAC Tests

#### TC-RBAC-001: Chef Cannot Access Reorders
- **Precondition**: Chef user logged in
- **Steps**: Attempt to access /reorders
- **Expected**: Access denied (403 or redirect)

#### TC-RBAC-002: Delivery Person Can Access Deliveries
- **Precondition**: Delivery person logged in
- **Steps**: Access /deliveries
- **Expected**: Delivery dashboard displayed

#### TC-RBAC-003: Admin Can Manage Users
- **Precondition**: Admin logged in
- **Steps**: Access /admin/users
- **Expected**: User management page displayed

## Performance Test Scenarios

### PT-001: Add Item Performance
- **Setup**: Database with 10,000 items
- **Action**: Add new item
- **Expected**: Response time < 2 seconds

### PT-002: Query Performance
- **Setup**: Database with 10,000 items
- **Action**: List all inventory items
- **Expected**: Response time < 1 second

### PT-003: Concurrent Users
- **Setup**: 20 concurrent users
- **Action**: All users perform inventory operations simultaneously
- **Expected**: All operations complete successfully, no performance degradation

### PT-004: Notification Delivery
- **Setup**: Item expiring within 3 days
- **Action**: Trigger notification check
- **Expected**: Notification created and available within 5 seconds

## Test Execution

### Running All Tests
```bash
pytest
```

### Running Unit Tests Only
```bash
pytest tests/unit/
```

### Running Integration Tests Only
```bash
pytest tests/integration/
```

### Running with Coverage
```bash
pytest --cov=app --cov-report=html
```

### Running Specific Test
```bash
pytest tests/unit/test_auth_service.py::test_authenticate_success
```

## Test Results

Test results are documented in `docs/testing/test_results.md` and include:
- Test execution summary
- Pass/fail statistics
- Coverage reports
- Performance metrics
- Screenshots of test execution

## Test Maintenance

- Tests are updated when features change
- New tests added for new features
- Broken tests fixed immediately
- Test coverage maintained above 80%
