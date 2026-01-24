# FFSmart User Manual

## Table of Contents

1. [Getting Started](#getting-started)
2. [User Roles](#user-roles)
3. [Features by Role](#features-by-role)
4. [Common Tasks](#common-tasks)
5. [Troubleshooting](#troubleshooting)

## Getting Started

### Accessing the System

1. Open your web browser and navigate to the FFSmart application URL
2. You will see the login page
3. Enter your username and password
4. Click "Login"

### First Time Login

If this is your first time logging in, you should:
- Change your password (if allowed by your role)
- Familiarize yourself with your dashboard
- Review available features for your role

## User Roles

### Head Chef
- Full access to all inventory features
- Can view and confirm reorders
- Receives notifications for expiring items and low stock
- Can manage chef accounts and access permissions
- Can view health and safety reports

### Chef
- Can view inventory
- Can add items to inventory
- Can remove items from inventory
- Limited access based on Head Chef configuration

### Delivery Person
- Can view assigned deliveries
- Can confirm deliveries
- Can request rear door access
- Can mark off delivered stock

### System Administrator
- Full system access
- Can manage all users
- Can view audit logs
- Can configure system settings

### Health & Safety Officer
- Read-only access to reports
- Can view compliance data
- Can export reports
- Can view expiry tracking

## Features by Role

### Inventory Management

#### Adding Items
1. Navigate to Inventory → Add Item
2. Fill in the form:
   - Item Name (required)
   - Quantity (required)
   - Supplier (optional)
   - Date Added (defaults to today)
   - Expiration Date (optional)
3. Click "Add Item"

#### Removing Items
1. Navigate to Inventory
2. Find the item you want to remove
3. Enter the quantity to remove
4. Click "Remove"

**Note**: You cannot remove more items than are available.

#### Viewing Inventory
- All users with inventory access can view the inventory list
- Items are color-coded:
  - **Red**: Expired items
  - **Yellow**: Expiring soon (within 3 days) or low stock
  - **White**: Normal items

### Notifications

#### Viewing Notifications
1. Click "Notifications" in the navigation bar
2. You will see all your notifications
3. Unread notifications are highlighted

#### Marking Notifications as Read
- Click "Mark as Read" on individual notifications
- Or click "Mark All as Read" to mark all notifications

#### Notification Types
- **Expiry Warning**: Items expiring within 3 days
- **Low Stock**: Items running low on quantity
- **Reorder Ready**: New reorder list generated

### Reorders (Head Chef Only)

#### Viewing Reorders
1. Navigate to Reorders
2. You will see all reorder lists
3. Click on a reorder to view details

#### Confirming Reorders
1. View the reorder details
2. Review the items to be reordered
3. Click "Confirm Reorder" if approved
4. Or click "Cancel Reorder" if not needed

#### Generating Reorders
- Reorders are automatically generated every Monday
- You can manually generate a reorder by clicking "Generate Reorder"

### Deliveries (Delivery Person)

#### Viewing Deliveries
1. Navigate to Deliveries
2. You will see all your assigned deliveries
3. Click on a delivery to view details

#### Confirming Deliveries
1. View the delivery details
2. Verify all items are correct
3. Click "Confirm Delivery"

#### Requesting Rear Door Access
1. Click "Request Rear Door Access" button
2. Access will be granted if you are authenticated
3. The system will log the access request

### User Management (Admin Only)

#### Creating Users
1. Navigate to Admin → Users
2. Click "Create User"
3. Fill in the form:
   - Username (required)
   - Email (required)
   - Password (required, minimum 6 characters)
   - Role (required)
4. Click "Create User"

#### Editing Users
1. Navigate to Admin → Users
2. Click "Edit" next to the user
3. Modify the information
4. Click "Update User"

#### Viewing Audit Logs
1. Navigate to Admin → Audit Logs
2. You will see all system actions
3. Logs show:
   - Timestamp
   - User who performed the action
   - Action type
   - Entity affected

## Common Tasks

### How to Check for Expiring Items
1. Log in as Head Chef
2. View your dashboard
3. The "Expiring Items" section shows items expiring in the next 3 days
4. Or navigate to Inventory to see all items with expiration warnings

### How to Handle Low Stock
1. You will receive a notification when items are low stock
2. View the inventory to see current quantities
3. Generate a reorder if needed (Head Chef only)
4. Or manually add items to inventory

### How to Export Reports (Health & Safety)
1. Log in as Health & Safety Officer
2. View your dashboard
3. Reports are displayed in tables
4. You can copy the data or take screenshots for export

## Troubleshooting

### Cannot Log In
- Verify your username and password are correct
- Check if your account is locked (too many failed attempts)
- Contact your administrator if issues persist

### Cannot See Certain Features
- Verify you have the correct role for the feature
- Some features are role-specific
- Contact your administrator if you believe you should have access

### Notifications Not Appearing
- Notifications are generated automatically
- Check if items actually meet the criteria (expiring within 3 days, low stock)
- Refresh the page to see new notifications

### Items Not Saving
- Verify all required fields are filled
- Check for duplicate items (same name, supplier, expiration date)
- If duplicate exists, the system will add to existing quantity instead

### Performance Issues
- Clear your browser cache
- Try refreshing the page
- Contact system administrator if problems persist

## Support

For additional support, please contact your system administrator or refer to the technical documentation.
