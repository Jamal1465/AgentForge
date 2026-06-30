"""Predefined domain packs for AgentForge.

Provides a registry of domain configurations used by DomainAnalyzer to supply
meaningful actors, entities, modules, and database structures.
"""

from __future__ import annotations

from agentforge.domain_analysis.domain_context import DomainContext

DOMAIN_PACKS: dict[str, DomainContext] = {
    "library-management": DomainContext(
        project_name="Library Management System",
        normalized_domain="library-management",
        domain_summary=(
            "The Library Management System will help educational institutions "
            "manage book cataloging, member registration, borrowing, returns, "
            "reservations, overdue fines, and reporting."
        ),
        actors=[
            "Student",
            "Faculty",
            "Librarian",
            "Administrator",
        ],
        entities=[
            "Book",
            "Book Copy",
            "Author",
            "Publisher",
            "Category",
            "Library Member",
            "Loan / Issue Record",
            "Reservation",
            "Fine",
            "Notification",
            "Library Branch",
            "Audit Log",
        ],
        workflows=[
            "Student/faculty registration",
            "Librarian adds and manages books",
            "Search and browse catalog",
            "Issue book",
            "Return book",
            "Renew borrowed book",
            "Reserve unavailable book",
            "Calculate overdue fines",
            "Manage damaged/lost books",
            "Generate inventory reports",
            "Generate overdue reports",
            "Manage member borrowing limits",
        ],
        modules=[
            "Authentication and Role Management",
            "Catalog Management",
            "Member Management",
            "Circulation Management",
            "Reservation Management",
            "Fine Management",
            "Reporting and Analytics",
            "Notification Management",
            "Audit and Administration",
        ],
        business_rules=[
            "Students can borrow a limited number of books.",
            "Faculty may have a higher borrowing limit than students.",
            "A book copy can only be issued if available.",
            "Overdue books generate fines based on configured fine rate.",
            "Reserved books cannot be issued to another member.",
            "Librarians can issue, return, renew, and manage books.",
            "Administrators can manage system settings, users, roles, and reports.",
        ],
        api_resources=[
            "/api/v1/auth/register",
            "/api/v1/auth/token",
            "/api/v1/members",
            "/api/v1/books",
            "/api/v1/catalog",
            "/api/v1/loans",
            "/api/v1/reservations",
            "/api/v1/fines",
        ],
        database_tables=[
            "users",
            "roles",
            "members",
            "books",
            "authors",
            "publishers",
            "categories",
            "book_copies",
            "loans",
            "reservations",
            "fines",
            "notifications",
            "audit_logs",
        ],
        reports=[
            "Overdue Loans Report",
            "Catalog Inventory and Stock Report",
            "Fine Collections and Audit Report",
        ],
        risks=[
            "wrong book availability count",
            "duplicate ISBN entries",
            "incorrect overdue fine calculation",
            "unauthorized access to member records",
            "data loss of circulation history",
            "book reservation conflicts",
        ],
        assumptions=[
            "Standard school/university operating hours",
            "Digital catalog database availability",
            "Reliable network connection inside library",
        ],
        out_of_scope=[
            "Inter-library loan system integration",
            "Automated book sorting machine control",
            "E-book reader hardware manufacturing",
        ],
        functional_requirements=[
            "FR-001 User Authentication and Role-Based Access",
            "FR-002 Student and Faculty Member Registration",
            "FR-003 Book Catalog Management",
            "FR-004 Book Copy Inventory Management",
            "FR-005 Search and Filter Books",
            "FR-006 Issue Book to Member",
            "FR-007 Return Book",
            "FR-008 Renew Borrowed Book",
            "FR-009 Reserve Book",
            "FR-010 Calculate Overdue Fine",
            "FR-011 Manage Lost or Damaged Book",
            "FR-012 Generate Overdue Report",
            "FR-013 Generate Inventory Report",
            "FR-014 Manage Librarian/Admin Settings",
            "FR-015 Audit Log Tracking",
        ],
        validation_rules=[
            "Book Validation: Title, ISBN, Author, Category are required. ISBN must match 13-digit pattern.",
            "Member Validation: Email must match standard format. Username length between 3 and 50 characters.",
            "Loan Validation: Book copy must be available (status = available). Member must not exceed limit.",
            "Reservation Validation: Book must have no available copies to reserve.",
            "Fine Validation: Fine amount must be non-negative.",
        ],
        edge_cases=[
            "EC-001: Concurrent issue of the last copy of a book copy. (Mitigation: Transaction isolation level SERIALIZABLE)",
            "EC-002: Member attempts to borrow a book while having unpaid overdue fines. (Mitigation: Reject loan if unpaid fines exist)",
            "EC-003: A book is returned damaged. (Mitigation: Librarian marks status as damaged and applies a fine)",
        ],
        request_response_examples="""### Register Book (POST `/api/v1/books`)
- **Request Payload**:
```json
{
  "isbn": "978-0-13-235088-4",
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "category": "Software Engineering"
}
```
- **Response Payload (HTTP 201 Created)**:
```json
{
  "id": "b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
  "isbn": "978-0-13-235088-4",
  "title": "Clean Code",
  "status": "available",
  "created_at": "2026-06-30T00:00:00Z"
}
```

### Issue Book Copy (POST `/api/v1/loans`)
- **Request Payload**:
```json
{
  "member_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
  "book_copy_id": "b1b2b3b4-c5c6-d7d8-e9e0-f1f2f3f4f5f6"
}
```
- **Response Payload (HTTP 201 Created)**:
```json
{
  "loan_id": "c2c3c4c5-d6d7-e8e9-f0f1-f2f3f4f5f6f7",
  "member_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
  "book_copy_id": "b1b2b3b4-c5c6-d7d8-e9e0-f1f2f3f4f5f6",
  "due_date": "2026-07-14T00:00:00Z",
  "status": "issued"
}
```""",
        authorization_matrix="""| Role | Member Register | Catalog Browse | Add Book | Issue Book | Manage Users |
|------|-----------------|----------------|----------|------------|--------------|
| Student | Yes (Own Only) | Yes | No | No | No |
| Faculty | Yes (Own Only) | Yes | No | No | No |
| Librarian | Yes | Yes | Yes | Yes | No |
| Administrator | Yes | Yes | Yes | Yes | Yes |""",
        traceability_matrix="""| Req ID | Module | Test Case ID | Target Release |
|--------|--------|--------------|----------------|
| FR-001 | Authentication | TC-AUTH-001 | v1.0.0 |
| FR-002 | Member Management | TC-MEMB-001 | v1.0.0 |
| FR-003 | Catalog Management | TC-CAT-001 | v1.0.0 |
| FR-006 | Circulation Management | TC-CIRC-001 | v1.0.0 |
| FR-009 | Reservation Management | TC-RES-001 | v1.0.0 |
| FR-010 | Fine Management | TC-FINE-001 | v1.0.0 |"""
    ),
    "task-management": DomainContext(
        project_name="Task Management System",
        normalized_domain="task-management",
        domain_summary=(
            "The Task Management System will help agile teams organize and track "
            "project sprint tasks, assignments, schedules, and custom board workflows."
        ),
        actors=[
            "Project Manager",
            "Team Lead",
            "Developer",
            "Viewer",
            "Administrator",
        ],
        entities=[
            "Project",
            "Task",
            "Sprint",
            "Comment",
            "Attachment",
            "Label",
            "User Profile",
            "Notification",
            "Activity Log",
        ],
        workflows=[
            "PM creates a new project and defines columns",
            "Developer is assigned a task and updates status",
            "Team Lead schedules a sprint and plans velocity",
            "System triggers email notification on task reassignment",
            "Administrator manages user roles and groups",
        ],
        modules=[
            "User Identity and Role Management",
            "Project Configuration and Workflow Board",
            "Task Lifecycle and Custom Fields",
            "Sprint Planning and Scheduling",
            "Collaborative Comments and Activity Stream",
            "Analytics and Team Velocity Reports",
        ],
        business_rules=[
            "Only project members can create tasks.",
            "Tasks cannot be closed without satisfying subtask checklist items.",
            "Sprints must be locked before starting.",
            "Administrators can override task locks.",
        ],
        api_resources=[
            "/api/v1/auth/register",
            "/api/v1/auth/token",
            "/api/v1/projects",
            "/api/v1/tasks",
            "/api/v1/sprints",
            "/api/v1/comments",
        ],
        database_tables=[
            "users",
            "roles",
            "projects",
            "tasks",
            "comments",
            "sprints",
            "labels",
            "activity_logs",
        ],
        reports=[
            "Sprint Burndown Chart Data",
            "Team Velocity Report",
            "Timesheet and Hours Report",
        ],
        risks=[
            "Task assignment confusion due to concurrent updates",
            "Over-allocation of developer sprint capacity",
            "Exposure of private repositories to external guest accounts",
        ],
        assumptions=[
            "Standard agile sprint cycles",
            "Internet access for team collaboration",
        ],
        out_of_scope=[
            "Integration with physical building security systems",
            "Automatic code generation from comments",
        ],
        functional_requirements=[
            "FR-001 User Registration and Role Authentication",
            "FR-002 Project Creation and Management",
            "FR-003 Task Lifecycle (CRUD)",
            "FR-004 Task Assignment",
            "FR-005 Sprint Scheduling and Planning",
            "FR-006 Board Visual Columns Configuration",
            "FR-007 Task Comments and Discussion",
            "FR-008 Task Dependency Linking",
            "FR-009 Time Tracking and Estimations",
            "FR-010 Notification and Alerts System",
            "FR-011 Generate Team Velocity Report",
            "FR-012 Generate Task Burndown Chart",
            "FR-013 Audit Log Logging",
        ],
        validation_rules=[
            "Task Validation: Title is mandatory. Priority must be low, medium, or high.",
            "Sprint Validation: Start date must be before end date.",
        ],
        edge_cases=[
            "EC-001: Assigning task to an inactive user. (Mitigation: Reject assignment)",
        ],
        request_response_examples="""### Create Task (POST `/api/v1/tasks`)
- **Request Payload**:
```json
{
  "title": "Build API",
  "project_id": "proj-uuid"
}
```
- **Response Payload**:
```json
{
  "id": "task-uuid",
  "title": "Build API",
  "status": "todo"
}
```""",
        authorization_matrix="""| Role | Create Project | Create Task | Update Status | Edit Board |
|------|---|---|---|---|
| Developer | No | Yes | Yes | No |
| PM | Yes | Yes | Yes | Yes |""",
        traceability_matrix="""| Req ID | Module | Test Case ID | Target Release |
|---|---|---|---|
| FR-003 | Task CRUD | TC-TASK-001 | v1.0.0 |"""
    ),
    "ecommerce": DomainContext(
        project_name="E-Commerce Platform",
        normalized_domain="ecommerce",
        domain_summary=(
            "The E-Commerce Platform provides robust customer cart management, "
            "product cataloging, checkout, secure payments, and order fulfillment."
        ),
        actors=[
            "Customer",
            "Merchant",
            "Inventory Manager",
            "Support Agent",
            "System Admin",
        ],
        entities=[
            "Product",
            "Cart",
            "Order",
            "Payment Transaction",
            "Customer Profile",
            "Coupon",
            "Review",
            "Shipment",
        ],
        workflows=[
            "Customer browses products and adds to cart",
            "Customer completes checkout and pays",
            "Merchant reviews order and fulfills shipment",
            "Inventory manager restocks low product copies",
            "Customer leaves product review and rating",
        ],
        modules=[
            "Product Catalog and Search",
            "Shopping Cart and Checkout",
            "Order Processing and State Engine",
            "Payment Gateway Integration",
            "Inventory Control and Alerts",
            "Shipping and Tracking",
        ],
        business_rules=[
            "Coupon discounts cannot exceed 100% of order value.",
            "Order total must match cart subtotal plus shipping.",
            "Cart items must hold stock reservation during checkout.",
            "Customers can only review products they purchased.",
        ],
        api_resources=[
            "/api/v1/auth/register",
            "/api/v1/auth/token",
            "/api/v1/products",
            "/api/v1/cart",
            "/api/v1/orders",
            "/api/v1/payments",
        ],
        database_tables=[
            "users",
            "roles",
            "products",
            "orders",
            "order_items",
            "payments",
            "carts",
            "shipments",
        ],
        reports=[
            "Daily Sales and Revenue Report",
            "Low Stock and Inventory Report",
            "Customer Retention Analytics",
        ],
        risks=[
            "Duplicate charge due to double click on checkout button",
            "Inaccurate inventory count leading to overselling products",
            "Unsafe credit card storage violating PCI-DSS compliance",
        ],
        assumptions=[
            "Valid currency rates and checkout processing",
            "Reliable payment processor uptime",
        ],
        out_of_scope=[
            "Offline retail POS cash register hardware integration",
            "Designing custom parcel delivery drones",
        ],
        functional_requirements=[
            "FR-001 Customer Registration and Authentication",
            "FR-002 Product Catalog and Search",
            "FR-003 Shopping Cart Management",
            "FR-004 Checkout Process",
            "FR-005 Payment Gateway Integration",
            "FR-006 Order Status Tracking",
            "FR-007 Inventory Restock Alerts",
            "FR-008 Customer Product Reviews",
            "FR-009 Shipping Rate Calculation",
            "FR-010 Discount Coupon Processing",
            "FR-011 Audit Log Tracking",
        ],
        validation_rules=[
            "Product Validation: Name and price are required. Price must be positive.",
            "Order Validation: Quantity must be greater than zero.",
        ],
        edge_cases=[
            "EC-001: Concurrent checkout of last inventory item. (Mitigation: Row locking)",
        ],
        request_response_examples="""### Create Order (POST `/api/v1/orders`)
- **Request Payload**:
```json
{
  "cart_id": "cart-uuid"
}
```
- **Response Payload**:
```json
{
  "id": "order-uuid",
  "status": "pending_payment"
}
```""",
        authorization_matrix="""| Role | Browse Products | Checkout | Manage Catalog | Refund |
|------|---|---|---|---|
| Customer | Yes | Yes | No | No |
| Merchant | Yes | No | Yes | Yes |""",
        traceability_matrix="""| Req ID | Module | Test Case ID | Target Release |
|---|---|---|---|
| FR-004 | Order Management | TC-ORD-001 | v1.0.0 |"""
    ),
    "learning-management-system": DomainContext(
        project_name="Learning Management System",
        normalized_domain="learning-management-system",
        domain_summary=(
            "The Learning Management System supports online educational course curriculum "
            "delivery, student enrollments, lessons, assessments, grading, and certifications."
        ),
        actors=[
            "Student",
            "Instructor",
            "Parent",
            "Registrar",
            "Administrator",
        ],
        entities=[
            "Course",
            "Lesson",
            "Quiz",
            "Enrollment",
            "Submission",
            "Grade",
            "Forum Post",
            "Certificate",
        ],
        workflows=[
            "Instructor creates course outline and uploads video",
            "Student enrolls in course",
            "Student completes lesson and submits quiz",
            "Instructor grades quiz and issues certificate",
            "Registrar pulls enrollment metrics",
        ],
        modules=[
            "Course Catalog and Curriculum Builder",
            "Enrollment and Registration",
            "Assessment and Quiz Engine",
            "Gradebook and Progression Tracker",
            "Discussion Forums and Peer Support",
            "Certifications and Analytics",
        ],
        business_rules=[
            "Quizzes must be completed before starting next lesson.",
            "Instructor must review subjective submissions.",
            "Student grades are private and only visible to them, instructor, and registrar.",
            "Certificates are issued only if final grade exceeds 70%.",
        ],
        api_resources=[
            "/api/v1/auth/register",
            "/api/v1/auth/token",
            "/api/v1/courses",
            "/api/v1/lessons",
            "/api/v1/quizzes",
            "/api/v1/enrollments",
            "/api/v1/grades",
        ],
        database_tables=[
            "users",
            "roles",
            "courses",
            "lessons",
            "quizzes",
            "enrollments",
            "submissions",
            "grades",
            "certificates",
        ],
        reports=[
            "Course Completion and Drop-out Report",
            "Student Average Gradebook Report",
            "Instructor Activity Audit",
        ],
        risks=[
            "Student cheating on online quizzes via duplicate browsers",
            "High bandwidth video loading bottleneck during peak hours",
            "Grade tampering by unauthorized accounts",
        ],
        assumptions=[
            "High-speed internet access for students",
            "Video streaming server availability",
        ],
        out_of_scope=[
            "On-campus dormitory room booking",
            "Selling physical printed textbooks",
        ],
        functional_requirements=[
            "FR-001 Course Creation and Outline Management",
            "FR-002 Student Registration and Course Enrollment",
            "FR-003 Lesson Content Delivery (Video/Text)",
            "FR-004 Quiz and Exam Submission Engine",
            "FR-005 Automated & Manual Assessment Grading",
            "FR-006 Course Certificate Generation",
            "FR-007 Forums and discussion board support",
        ],
        validation_rules=[
            "Course Validation: Course title is mandatory.",
            "Grade Validation: Grade value must be between 0 and 100.",
        ],
        edge_cases=[
            "EC-001: Video player fails due to slow student connection. (Mitigation: Quality fallback)",
        ],
        request_response_examples="""### Enroll In Course (POST `/api/v1/enrollments`)
- **Request Payload**:
```json
{
  "course_id": "course-uuid"
}
```
- **Response Payload**:
```json
{
  "id": "enrollment-uuid",
  "status": "active"
}
```""",
        authorization_matrix="""| Role | View Lessons | Submit Quizzes | Edit Syllabus | Grade Submissions |
|------|---|---|---|---|
| Student | Yes | Yes | No | No |
| Instructor | Yes | No | Yes | Yes |""",
        traceability_matrix="""| Req ID | Module | Test Case ID | Target Release |
|---|---|---|---|
| FR-002 | Course Enrollment | TC-ENR-001 | v1.0.0 |"""
    ),
    "hospital-management": DomainContext(
        project_name="Hospital Management System",
        normalized_domain="hospital-management",
        domain_summary=(
            "The Hospital Management System manages electronic medical records (EMR), "
            "patient portals, clinical consultations, doctor appointments, billing, and pharmacy."
        ),
        actors=[
            "Patient",
            "Doctor",
            "Nurse",
            "Pharmacist",
            "Billing Specialist",
            "Administrator",
        ],
        entities=[
            "Patient Record",
            "Medical History",
            "Appointment",
            "Prescription",
            "Bill / Invoice",
            "Lab Test Result",
            "Room",
            "Ward",
            "Staff Schedule",
            "Audit Trail",
        ],
        workflows=[
            "Patient registers and requests appointment",
            "Doctor checks patient, updates medical history, and writes prescription",
            "Lab technician uploads test results",
            "Billing specialist calculates treatment costs and issues invoice",
            "Pharmacist verifies prescription and dispenses medicine",
        ],
        modules=[
            "Patient Portal and Scheduling",
            "Electronic Medical Records (EMR)",
            "Clinical Workflows and Consultations",
            "Billing and Insurance Claims",
            "Pharmacy and Laboratory Integration",
            "Hospital Resource and Ward Management",
        ],
        business_rules=[
            "Doctor schedules cannot overlap.",
            "Patient records must be encrypted to comply with HIPAA guidelines.",
            "Only authorized staff can view clinical medical records.",
            "Prescription changes are logged with digital signatures.",
        ],
        api_resources=[
            "/api/v1/auth/register",
            "/api/v1/auth/token",
            "/api/v1/patients",
            "/api/v1/appointments",
            "/api/v1/prescriptions",
            "/api/v1/invoices",
            "/api/v1/lab-results",
        ],
        database_tables=[
            "users",
            "roles",
            "patients",
            "appointments",
            "prescriptions",
            "invoices",
            "lab_results",
            "rooms",
            "audit_logs",
        ],
        reports=[
            "Daily Invoice and Billing Summary",
            "Patient Admission and Discharge Log",
            "Lab Test Turnaround Audit",
        ],
        risks=[
            "Exposure of protected health information (PHI) violating HIPAA",
            "Scheduling collision for surgery rooms",
            "Inaccurate prescription dosage entry by staff",
        ],
        assumptions=[
            "Standard regulatory compliance guidelines are active",
            "Medical staff are trained in data entry",
        ],
        out_of_scope=[
            "Designing surgical robotics firmware",
            "Ambulance vehicle fleet maintenance",
        ],
        functional_requirements=[
            "FR-001 Electronic Health Record (EHR) encryption",
            "FR-002 Patient Appointment Booking Scheduler",
            "FR-003 Doctor Clinical Notes entry portal",
            "FR-004 Lab results document upload",
            "FR-005 Medication Prescription issuance",
            "FR-006 Billing invoice creation",
            "FR-007 Audit Trail of EMR logs",
        ],
        validation_rules=[
            "Patient Validation: Date of birth is required.",
            "Invoice Validation: Bill details must sum to total.",
        ],
        edge_cases=[
            "EC-001: Access of medical records during emergency. (Mitigation: Break-glass override log)",
        ],
        request_response_examples="""### Book Appointment (POST `/api/v1/appointments`)
- **Request Payload**:
```json
{
  "doctor_id": "doc-uuid",
  "appointment_time": "2026-06-30T10:00:00Z"
}
```
- **Response Payload**:
```json
{
  "id": "appt-uuid",
  "status": "scheduled"
}
```""",
        authorization_matrix="""| Role | View EMR | Write Prescription | View Billing | Schedule Doctor |
|------|---|---|---|---|
| Patient | Yes (Own) | No | Yes (Own) | No |
| Doctor | Yes | Yes | No | No |""",
        traceability_matrix="""| Req ID | Module | Test Case ID | Target Release |
|---|---|---|---|
| FR-001 | EHR Management | TC-EMR-001 | v1.0.0 |"""
    ),
    "inventory-management": DomainContext(
        project_name="Inventory Management System",
        normalized_domain="inventory-management",
        domain_summary=(
            "The Inventory Management System manages warehouse stock levels, purchase "
            "orders, sales orders, suppliers, reorder policies, and fulfillment dispatching."
        ),
        actors=[
            "Inventory Manager",
            "Purchase Agent",
            "Receiver",
            "Dispatcher",
            "Vendor",
            "System Admin",
        ],
        entities=[
            "Product",
            "Stock Item",
            "Warehouse",
            "Purchase Order",
            "Sales Order",
            "Supplier",
            "Inventory Transaction",
            "Stock Alert",
            "Reorder Policy",
        ],
        workflows=[
            "Purchase agent issues purchase order to vendor",
            "Receiver receives stock copy at warehouse and scans barcode",
            "Dispatcher packs and ships sales order items",
            "System triggers stock alert when inventory level falls below reorder point",
            "Manager updates supplier catalogs",
        ],
        modules=[
            "Warehouse and Location Control",
            "Stock Inventory Management",
            "Purchase Order Processing",
            "Fulfillment and Barcode Dispatching",
            "Supplier/Vendor Catalog",
            "Alerts and Automatic Reordering",
        ],
        business_rules=[
            "Inventory balance cannot go below zero.",
            "Reorders are sent automatically when current stock is below reorder point.",
            "Barcode scans must verify correct items before shipping.",
            "Only purchase agents can authorize orders above $10,000.",
        ],
        api_resources=[
            "/api/v1/auth/register",
            "/api/v1/auth/token",
            "/api/v1/inventory",
            "/api/v1/purchase-orders",
            "/api/v1/suppliers",
            "/api/v1/warehouses",
        ],
        database_tables=[
            "users",
            "roles",
            "inventory_items",
            "warehouses",
            "purchase_orders",
            "suppliers",
            "stock_transactions",
            "alerts",
        ],
        reports=[
            "Current Stock Valuation Report",
            "Supplier Delivery Performance Audit",
            "Restock and Reorder Purchase Queue",
        ],
        risks=[
            "Warehouse stock count mismatch between physical shelf and database",
            "Unnotified supplier delay leading to stockout",
            "Spoilage or expiration of batch items",
        ],
        assumptions=[
            "Barcode hardware compatibility",
            "Single timezone warehouse synchronization",
        ],
        out_of_scope=[
            "Manufacturing floor automation and PLC assembly",
            "Operating delivery vehicle fleets",
        ],
        functional_requirements=[
            "FR-001 Warehouse and Storage Location Mapping",
            "FR-002 Supplier/Vendor Contact Directory",
            "FR-003 Stock SKU creation and tracking",
            "FR-004 Barcode scan item receiving",
            "FR-005 Sales order packing checklist",
            "FR-006 Automatic Reorder email alert",
            "FR-007 Stock balance transaction history",
        ],
        validation_rules=[
            "SKU Validation: SKU code must be unique.",
            "Supplier Validation: Phone and email must be provided.",
        ],
        edge_cases=[
            "EC-001: Incorrect barcode scan. (Mitigation: Block submission and play alert sound)",
        ],
        request_response_examples="""### Restock Stock (POST `/api/v1/inventory`)
- **Request Payload**:
```json
{
  "sku": "SKU-AUTO-998",
  "quantity": 150
}
```
- **Response Payload**:
```json
{
  "sku": "SKU-AUTO-998",
  "current_quantity": 420,
  "status": "updated"
}
```""",
        authorization_matrix="""| Role | Scan Stock | View Inventory | Edit Reorder Limit | Create Vendor |
|------|---|---|---|---|
| Dispatcher | Yes | Yes | No | No |
| Manager | Yes | Yes | Yes | Yes |""",
        traceability_matrix="""| Req ID | Module | Test Case ID | Target Release |
|---|---|---|---|
| FR-003 | SKU Management | TC-SKU-001 | v1.0.0 |"""
    ),
    "generic-business-app": DomainContext(
        project_name="Business Application",
        normalized_domain="generic-business-app",
        domain_summary=(
            "A secure enterprise application to manage resources, user roles, "
            "business workflows, audit logs, and analytics dashboard reports."
        ),
        actors=[
            "Standard User",
            "Supervisor",
            "Administrator",
            "Guest",
        ],
        entities=[
            "Core Record",
            "Resource Category",
            "User Profile",
            "Transaction Log",
            "Activity Event",
            "Attachment",
            "Custom Field",
            "Configuration Parameter",
        ],
        workflows=[
            "User creates a new resource record",
            "Supervisor reviews and approves resource status",
            "User updates details and files attachment",
            "System records audit log entry of modification",
            "Admin updates system settings",
        ],
        modules=[
            "Core Application Portal and Dashboards",
            "Identity, Authentication, and Permissions",
            "Business Resource Management",
            "Workflow Stages and State Control",
            "Reports and Export Engines",
            "Audit Logs and System Administration",
        ],
        business_rules=[
            "Record creation requires valid category and owner fields.",
            "Modifications to approved records require supervisor review.",
            "Deletion is restricted to system administrators.",
        ],
        api_resources=[
            "/api/v1/auth/register",
            "/api/v1/auth/token",
            "/api/v1/resources",
            "/api/v1/approvals",
            "/api/v1/audit-logs",
        ],
        database_tables=[
            "users",
            "roles",
            "resources",
            "categories",
            "audit_logs",
            "settings",
        ],
        reports=[
            "Monthly Activity and Resource Count Summary",
            "System Configuration and Access Audit Log",
        ],
        risks=[
            "Unauthorized access to private organization records",
            "Database locks due to concurrent transaction spikes",
            "Data corruption during bulk import operations",
        ],
        assumptions=[
            "Modern web browser compatibility",
            "Stateless API architecture",
        ],
        out_of_scope=[
            "Complex hardware sensor integration",
            "Multi-lingual physical translation agency management",
        ],
        functional_requirements=[
            "FR-001 User Account Registration and Authentication",
            "FR-002 Resource Management CRUD Workflows",
            "FR-003 Resource Ownership Assignment",
            "FR-004 Attachment upload file management",
            "FR-005 State Machine workflow transitions",
            "FR-006 Supervisor approval workflows",
            "FR-007 System configuration options",
        ],
        validation_rules=[
            "Resource Validation: Category is required.",
        ],
        edge_cases=[
            "EC-001: Deleting critical system configuration. (Mitigation: Require Master admin confirmation)",
        ],
        request_response_examples="""### Create Resource (POST `/api/v1/resources`)
- **Request Payload**:
```json
{
  "name": "Record A"
}
```
- **Response Payload**:
```json
{
  "id": "uuid",
  "name": "Record A"
}
```""",
        authorization_matrix="""| Role | View Records | Create Records | Approve Changes | Edit Settings |
|------|---|---|---|---|
| Standard | Yes | Yes | No | No |
| Admin | Yes | Yes | Yes | Yes |""",
        traceability_matrix="""| Req ID | Module | Test Case ID | Target Release |
|---|---|---|---|
| FR-002 | CRUD Workflow | TC-CRUD-001 | v1.0.0 |"""
    ),
}
