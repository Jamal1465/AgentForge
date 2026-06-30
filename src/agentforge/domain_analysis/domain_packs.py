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
        institution_context="University Library Administration Environment",
        primary_users=["Student", "Faculty Member"],
        secondary_users=["Librarian", "Administrator"],
        actors=[
            "Student",
            "Faculty Member",
            "Librarian",
            "Administrator",
        ],
        actors_with_responsibilities={
            "Student": "search catalog, reserve books, view loans, view fines, receive due-date notifications.",
            "Faculty Member": "borrow books with extended limits, reserve books, view borrowing history.",
            "Librarian": "manage catalog, manage book copies, issue books, return books, renew loans, manage reservations, collect fines.",
            "Administrator": "manage users, roles, library policies, fine rates, borrowing limits, audit logs, and reports.",
        },
        domain_problems=[
            "Manual book issue/return tracking causes errors.",
            "Book availability is difficult to maintain accurately.",
            "Students and faculty cannot easily check availability or reserve books.",
            "Librarians need reliable overdue, fine, and inventory reports.",
            "Duplicate ISBN entries and missing copy-level tracking create catalog inconsistencies.",
            "Paper-based circulation history is hard to audit.",
        ],
        business_goals=[
            "Centralize catalog and physical copy inventory.",
            "Automate book issue, return, renewal, reservation, and fine calculation.",
            "Provide role-based access for students, faculty, librarians, and administrators.",
            "Improve visibility into available, borrowed, reserved, damaged, and lost books.",
            "Generate accurate overdue, circulation, and inventory reports.",
            "Maintain full audit history for circulation actions.",
        ],
        measurable_success_criteria=[
            "Catalog search p95 latency stays under 300ms.",
            "100% of book issue and return transactions are recorded in the audit log.",
            "Zero duplicate active loans are allowed for the same book copy.",
            "Overdue reports are generated automatically and accurately daily.",
            "Role-based access is strictly enforced for all administrative and circulation endpoints.",
            "Book copy status remains consistent across loans, returns, and reservations.",
        ],
        entities=[
            "User",
            "Role",
            "Student",
            "Faculty Member",
            "Librarian",
            "Book",
            "Book Copy",
            "Author",
            "Publisher",
            "Category",
            "Loan",
            "Reservation",
            "Fine",
            "Notification",
            "Library Policy",
            "Audit Log",
        ],
        workflows=[
            "Register student/faculty member",
            "Add/update book metadata",
            "Add/manage physical book copies",
            "Search and filter catalog",
            "Issue available book copy",
            "Return borrowed book",
            "Renew active loan",
            "Reserve unavailable book",
            "Calculate overdue fine",
            "Mark book as lost or damaged",
            "Generate overdue report",
            "Generate inventory report",
            "Configure borrowing limits and fine rates",
        ],
        modules=[
            "Authentication and Role Management",
            "Member Management",
            "Catalog Management",
            "Book Copy Inventory Management",
            "Circulation Management",
            "Reservation Management",
            "Fine Management",
            "Notification Management",
            "Reporting and Analytics",
            "Administration and Audit Logs",
        ],
        business_rules=[
            "Students can borrow a limited number of books.",
            "Faculty members borrow books with extended limits.",
            "A book copy can only be issued if its status is available.",
            "Overdue books generate fines based on configured fine rate policies.",
            "Reserved books cannot be issued to another member until the reservation expires.",
            "Librarians can issue, return, renew, and manage books.",
            "Administrators manage system settings, fine rates, borrowing limits, and audit logs.",
        ],
        functional_requirements=[
            "FR-001 Authentication and RBAC",
            "FR-002 Student and Faculty Member Management",
            "FR-003 Book Catalog Management",
            "FR-004 Book Copy Inventory Management",
            "FR-005 Search and Filter Catalog",
            "FR-006 Issue Book",
            "FR-007 Return Book",
            "FR-008 Renew Loan",
            "FR-009 Reserve Book",
            "FR-010 Overdue Fine Calculation",
            "FR-011 Lost/Damaged Book Handling",
            "FR-012 Notifications",
            "FR-013 Overdue Report",
            "FR-014 Inventory Report",
            "FR-015 Audit Log Tracking",
        ],
        non_functional_requirements=[
            "Catalog search latency under 300ms for p95 requests.",
            "Loan transaction atomicity (loans, returns, renewals must be atomic).",
            "Book copy inventory consistency across active circulation states.",
            "Role-based access enforcement for sensitive library functions.",
            "Auditability of issue/return transactions.",
            "Secure backup and recovery of all circulation records.",
            "High availability during university library operating hours (99.9% uptime).",
            "Data privacy compliance for student and faculty borrowing history records.",
        ],
        feasibility_points={
            "technical": "Highly feasible. Catalog indexing is optimized via SQL indexes. Copy-level inventory and concurrent loan/reservation transaction handling utilize database ACID transactions. Fine calculation algorithms compute overdue penalties securely, and reporting queries are optimized.",
            "operational": "Replaces paper logs with librarian workflow improvement. Provides student/faculty self-service portals to search and reserve books. Admin policy management controls borrowing limits, and training needs are minimal.",
            "economic": "Extremely cost-effective. Leads to reduced manual work and reduced record loss. Relies on open-source deployment tools (Docker/PostgreSQL), matching university budget suitability.",
            "schedule": "Feasible to deliver in phases based on real modules: RBAC, catalog, member management, circulation, reservations, fines, reports, notifications, deployment.",
            "legal": "Secures student/faculty record privacy. Maintains immutable audit logs and strict access control, ensuring backup retention.",
        },
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
            "library_policies",
            "audit_logs",
        ],
        reports=[
            "Overdue Loans Report",
            "Active Reservations Summary",
            "Branch Copy Inventory Status",
            "Fines Collected Ledger",
            "Circulation Frequency Report",
        ],
        risks=[
            "Wrong availability count.",
            "Duplicate ISBN/book copy entries.",
            "Incorrect fine calculation.",
            "Unauthorized access to member records.",
            "Lost circulation history.",
            "Reservation conflicts.",
        ],
        assumptions=[
            "Physical books contain readable ISBN barcodes.",
            "Users have access to university web browsers.",
            "Database connectivity remains persistent.",
        ],
        constraints=[
            "Must deploy on local university virtual machine architecture.",
            "Uptime must meet 99.9% library operational hours SLA.",
            "Authentication must integrate with role-based policies.",
        ],
        out_of_scope=[
            "Physical purchase ordering of new book stocks.",
            "General book shipping, mailing, or delivery services.",
            "Inter-library loans with other university networks.",
        ],
        validation_rules=[
            "Book Validation: Title, ISBN, Author, Category are required. ISBN must match 13-digit pattern.",
            "Member Validation: Email must match standard format. Username length between 3 and 50 characters.",
            "Loan Validation: Book copy must be available (status = available). Member must not exceed limit.",
            "Reservation Validation: Book must have no available copies to reserve.",
            "Fine Validation: Fine amount must be non-negative.",
        ],
        edge_cases=[
            "EC-001: Concurrent issue of the last copy of a book. (Mitigation: Transaction isolation level SERIALIZABLE)",
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
```""",
        authorization_matrix="""| Role | Member Register | Catalog Browse | Add Book | Issue Book | Manage Users |
|------|-----------------|----------------|----------|------------|--------------|
| Student | Yes (Own Only) | Yes | No | No | No |
| Faculty Member | Yes (Own Only) | Yes | No | No | No |
| Librarian | Yes | Yes | Yes | Yes | No |
| Administrator | Yes | Yes | Yes | Yes | Yes |""",
        traceability_matrix="""| Req ID | Component / Service | Database Table | Verification Method |
|--------|---------------------|----------------|---------------------|
| FR-001 | Auth Service | users, roles | Integration Test |
| FR-003 | Catalog Service | books, authors | Unit Test |
| FR-006 | Circulation Service | loans | System Test |
| FR-010 | Fine Service | fines | Unit Test |""",
    ),
    "ecommerce": DomainContext(
        project_name="Ecommerce Store",
        normalized_domain="ecommerce",
        domain_summary=(
            "The Ecommerce Store provides digital catalog browsing, cart operations, "
            "secure checkout, payment gateway processing, order fulfillment, and inventory control."
        ),
        institution_context="Commercial Retail Sales Environment",
        primary_users=["Customer"],
        secondary_users=["Merchant", "Store Admin"],
        actors=["Customer", "Merchant", "Store Admin"],
        actors_with_responsibilities={
            "Customer": "Browse product catalog, add products to shopping cart, proceed to checkout, make payment, track order status.",
            "Merchant": "Create and update product listings, manage inventory levels, process shipments, view store analytics.",
            "Store Admin": "Manage system configurations, user accounts, payment gateway credentials, and audit logs.",
        },
        domain_problems=[
            "Slow product catalog load times reduce conversions.",
            "Over-selling of products due to concurrent checkout operations.",
            "Lack of real-time shipment and delivery status tracking.",
            "Security risks with raw payment detail storage.",
        ],
        business_goals=[
            "Establish a responsive digital store front.",
            "Provide transactional consistency for shopping cart checkout and inventory decrement.",
            "Integrate secure third-party payment processing.",
            "Enable simple order fulfillment and tracking tools.",
        ],
        measurable_success_criteria=[
            "Catalog browse latency is under 250ms for p95 requests.",
            "Zero instances of over-selling products (strict inventory constraints).",
            "99.9% successful payment operations using external gateway adapters.",
            "Order updates automatically push tracking notifications to customers.",
        ],
        entities=[
            "Customer Profile",
            "Product Catalog",
            "Product Variant",
            "Shopping Cart",
            "Cart Item",
            "Checkout Session",
            "Order Record",
            "OrderItem",
            "Payment Gateway Transaction",
            "Shipment Details",
            "Inventory Stock",
        ],
        workflows=[
            "Browse product catalog",
            "Search and filter products",
            "Add product to shopping cart",
            "Modify cart items",
            "Submit checkout details",
            "Authorize payment transaction",
            "Decrement inventory levels",
            "Fulfill order and generate shipment",
            "Track order shipment status",
        ],
        modules=[
            "Authentication and Role Management",
            "Product Catalog Management",
            "Shopping Cart and Checkout",
            "Payment Gateway Integration",
            "Order Fulfillment and Tracking",
            "Inventory Control and Alerts",
            "Sales Reporting and Analytics",
        ],
        business_rules=[
            "Products can only be added to cart if stock is greater than zero.",
            "Checkout creates an order in pending state until payment is verified.",
            "Inventory must be locked during checkout to prevent concurrent over-selling.",
            "Payments must be routed through PCI-compliant gateway adapters.",
            "Only Store Admins can modify store settings and retrieve financial reports.",
        ],
        functional_requirements=[
            "FR-001 Customer Registration and Profiles",
            "FR-002 Product Catalog Management",
            "FR-003 Search and Filter Catalog",
            "FR-004 Shopping Cart Operations",
            "FR-005 Checkout Flow Processing",
            "FR-006 Payment Gateway Integration",
            "FR-007 Order Record Creation",
            "FR-008 Real-Time Inventory Control",
            "FR-009 Order Fulfillment",
            "FR-010 Order Status Tracking",
        ],
        non_functional_requirements=[
            "Catalog query latency under 250ms for p95 requests.",
            "Inventory decrement transaction isolation (ACID compliant).",
            "PCI-DSS compliance for payment integrations.",
            "High availability of checkout services during sale events (99.99% uptime).",
            "Encryption of user profiles and transaction data.",
        ],
        feasibility_points={
            "technical": "Highly feasible. Catalog caching provides fast query speeds. Inventory tracking is secured with PostgreSQL transaction locks. Payments use standard Stripe/PayPal APIs.",
            "operational": "Improves order tracking for customers and automates inventory tasks. Requires minimal staff training for fulfilling order shipments.",
            "economic": "Extremely viable. Low startup costs. Open-source deployment reduces license fees. Pay-as-you-go payment processing.",
            "schedule": "Feasible for 6-week completion. Phase 1: Catalog & Cart (Weeks 1-2). Phase 2: Checkout & Payment (Weeks 3-4). Phase 3: Fulfillment & Inventory (Week 5). Phase 4: Integration Test & Deployment (Week 6).",
            "legal": "Requires strict data compliance for customer records and PCI-compliant payment integrations.",
        },
        api_resources=[
            "/api/v1/auth/register",
            "/api/v1/auth/token",
            "/api/v1/products",
            "/api/v1/cart",
            "/api/v1/checkout",
            "/api/v1/payments/webhook",
            "/api/v1/orders",
        ],
        database_tables=[
            "users",
            "roles",
            "products",
            "product_variants",
            "carts",
            "cart_items",
            "orders",
            "order_items",
            "payments",
            "shipments",
            "inventory",
        ],
        reports=[
            "Daily Sales Revenue Report",
            "Inventory Low Stock Alerts",
            "Product Popularity Matrix",
            "Payment Reconciliation Ledger",
        ],
        risks=[
            "Slow database performance during high checkout volume.",
            "External payment gateway outage.",
            "Inventory discrepancies due to failed rollback actions.",
        ],
        assumptions=[
            "Payment processors provide webhook events.",
            "Merchant manages physical stock logistics.",
        ],
        constraints=[
            "Must support standard modern web browsers.",
            "Must comply with external API rate limits.",
        ],
        out_of_scope=[
            "Direct physical shipping and freight logistics.",
            "Supplier billing and wholesale contract management.",
        ],
        validation_rules=[
            "Product Validation: Title, price, and stock count must be valid.",
            "Payment Validation: Transaction ID and token must match format.",
            "Order Validation: Order must contain at least one item with positive quantity.",
        ],
        edge_cases=[
            "EC-001: Product stock reaches zero while in customer cart. (Mitigation: Re-validate stock at checkout)",
            "EC-002: Double payment callback received. (Mitigation: Idempotent payment processing logic)",
        ],
        request_response_examples="""### Submit Checkout (POST `/api/v1/checkout`)
- **Request Payload**:
```json
{
  "cart_id": "c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
  "shipping_address": "123 Main St",
  "payment_method": "stripe_token"
}
```
- **Response Payload (HTTP 200 OK)**:
```json
{
  "order_id": "d98fb91f-0b0c-4e8b-a25e-e099bc11a43a",
  "status": "pending_payment",
  "total_amount": 99.99
}
```""",
        authorization_matrix="""| Role | View Products | Add to Cart | Update Inventory | Process Orders |
|------|---------------|-------------|------------------|----------------|
| Customer | Yes | Yes | No | No |
| Merchant | Yes | No | Yes | Yes |
| Store Admin | Yes | No | Yes | Yes |""",
        traceability_matrix="""| Req ID | Component / Service | Database Table | Verification Method |
|--------|---------------------|----------------|---------------------|
| FR-002 | Product Service | products | Unit Test |
| FR-004 | Cart Service | carts, cart_items| Unit Test |
| FR-006 | Payment Service | payments | Mock Integration Test |""",
    ),
    "hospital-management": DomainContext(
        project_name="Hospital Management System",
        normalized_domain="hospital-management",
        domain_summary=(
            "The Hospital Management System coordinates patient registration, medical records, "
            "doctor scheduling, clinical appointments, prescriptions, and billing operations."
        ),
        institution_context="Clinical Medical Care Environment",
        primary_users=["Patient"],
        secondary_users=["Doctor", "Receptionist", "Administrator"],
        actors=["Patient", "Doctor", "Receptionist", "Administrator"],
        actors_with_responsibilities={
            "Patient": "Register account, request clinical appointments, view electronic medical records (EMR), view prescriptions, pay bills.",
            "Doctor": "Manage patient lists, update medical records, write clinical prescriptions, manage shift schedule.",
            "Receptionist": "Check patient registration, schedule appointments, process billing payments, verify insurance.",
            "Administrator": "Manage hospital staff, system settings, departments, audit logs, and compliance logs.",
        },
        domain_problems=[
            "Errors in manual patient record-keeping.",
            "Double-booking of doctors or clinic rooms.",
            "Lack of secure, centralized access to medical history.",
            "Delays in clinical prescription fulfillment.",
        ],
        business_goals=[
            "Establish a secure, central EMR database.",
            "Provide automated appointment scheduling with zero double-booking.",
            "Enforce HIPAA compliance and patient record privacy rules.",
            "Provide clean billing and invoicing tools.",
        ],
        measurable_success_criteria=[
            "EMR queries return patient history in under 300ms.",
            "Zero appointment double-bookings (strict room/doctor calendar constraints).",
            "100% of medical record edits are logged in compliance audit trails.",
            "Billing alerts automatically push invoicing to patients upon discharge.",
        ],
        entities=[
            "User Profile",
            "Patient Profile",
            "Doctor Profile",
            "Medical Record",
            "Appointment Slot",
            "Prescription",
            "Invoice Record",
            "Insurance Claim",
            "Clinical Room",
            "Compliance Log",
        ],
        workflows=[
            "Register patient profile",
            "Schedule clinical appointment",
            "View electronic medical record",
            "Update patient medical history",
            "Write electronic prescription",
            "Generate invoice billing",
            "Approve compliance audit log",
        ],
        modules=[
            "Authentication and Role Management",
            "Patient EMR Management",
            "Appointment Scheduling",
            "Clinical Prescription Management",
            "Billing and Insurance",
            "Hospital Staff Scheduling",
            "Compliance and Audit Logs",
        ],
        business_rules=[
            "Only doctors can write prescriptions and update patient medical records.",
            "Receptionists can book appointments but cannot read EMR clinical details.",
            "Patients can only view their own medical records and billing history.",
            "Appointments must check doctor availability before confirmation.",
            "Compliance logs are immutable and cannot be deleted or modified.",
        ],
        functional_requirements=[
            "FR-001 Patient Registration and Portals",
            "FR-002 Doctor Profiles and Schedules",
            "FR-003 EMR Patient Medical History",
            "FR-004 Appointment Scheduling",
            "FR-005 Doctor Availability Checks",
            "FR-006 Electronic Prescriptions",
            "FR-007 Invoicing and Billing",
            "FR-008 Insurance Verification",
            "FR-009 Immutable Compliance Logs",
            "FR-010 Patient Portals",
        ],
        non_functional_requirements=[
            "EMR query latency under 300ms for p95 requests.",
            "Strict compliance audit logs (immutable).",
            "HIPAA patient record privacy compliance.",
            "High availability for emergency EMR access (99.99% uptime).",
            "Encryption of sensitive clinical health identifiers.",
        ],
        feasibility_points={
            "technical": "Highly feasible. Medical records use secure database engines with row-level encryption. Scheduling logic uses calendar check procedures. Compliance logs use write-once ledgers.",
            "operational": "Speeds receptionist scheduling tasks and eliminates paper record errors. Simple training is required for doctors and clinical staff.",
            "economic": "Extremely viable. Lowers paperwork costs and prevents billing errors. Uptime requirements fit standard server budgets.",
            "schedule": "Feasible for 8-week delivery. Weeks 1-2: EMR & RBAC. Weeks 3-4: Scheduling. Weeks 5-6: Prescriptions & Invoices. Weeks 7-8: Compliance & Testing.",
            "legal": "Requires strict legal compliance with patient privacy laws (HIPAA/GDPR) and detailed system access audit trails.",
        },
        api_resources=[
            "/api/v1/auth/register",
            "/api/v1/auth/token",
            "/api/v1/patients",
            "/api/v1/appointments",
            "/api/v1/emr",
            "/api/v1/prescriptions",
            "/api/v1/billing",
        ],
        database_tables=[
            "users",
            "roles",
            "patients",
            "doctors",
            "appointments",
            "emr_records",
            "prescriptions",
            "billing_records",
            "compliance_logs",
        ],
        reports=[
            "Doctor Utilization Summary",
            "Daily Billing Summary",
            "Compliance Access Audits",
            "Prescription Distribution Stats",
        ],
        risks=[
            "System offline during clinical emergency.",
            "Unauthorized EMR data access leak.",
            "Incorrect prescription dosage notation.",
        ],
        assumptions=[
            "Doctors have electronic network terminals.",
            "Patients have internet/mobile access.",
        ],
        constraints=[
            "Uptime must meet critical clinical environment levels.",
            "Integration with national health databases.",
        ],
        out_of_scope=[
            "Hospital pharmaceutical supply chain management.",
            "Physical room security monitoring.",
        ],
        validation_rules=[
            "Patient Validation: Social security or medical ID is required.",
            "Prescription Validation: Dosage and drug name must be specified.",
            "Appointment Validation: Slot must be within active hours.",
        ],
        edge_cases=[
            "EC-001: Access of medical records during emergency. (Mitigation: Break-glass override log policy)",
            "EC-002: Overlapping appointment request. (Mitigation: Database row lock on doctor schedule)",
        ],
        request_response_examples="""### Book Appointment (POST `/api/v1/appointments`)
- **Request Payload**:
```json
{
  "doctor_id": "d0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
  "patient_id": "b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22",
  "appointment_time": "2026-06-30T10:00:00Z"
}
```
- **Response Payload (HTTP 201 Created)**:
```json
{
  "id": "e98fb91f-0b0c-4e8b-a25e-e099bc11a43a",
  "status": "scheduled",
  "appointment_time": "2026-06-30T10:00:00Z"
}
```""",
        authorization_matrix="""| Role | View EMR | Write Prescription | View Billing | Schedule Doctor |
|------|---|---|---|---|
| Patient | Yes (Own) | No | Yes (Own) | No |
| Doctor | Yes | Yes | No | Yes |
| Receptionist | No | No | Yes | Yes |
| Administrator | Yes | No | Yes | Yes |""",
        traceability_matrix="""| Req ID | Component / Service | Database Table | Verification Method |
|--------|---------------------|----------------|---------------------|
| FR-003 | EMR Service | emr_records | Unit Test |
| FR-004 | Appointment Service | appointments | Integration Test |
| FR-006 | Prescription Service| prescriptions | Unit Test |""",
    ),
    "learning-management-system": DomainContext(
        project_name="Learning Management System",
        normalized_domain="learning-management-system",
        domain_summary=(
            "The Learning Management System coordinates course publishing, student enrollments, "
            "lesson delivery, assignment submissions, grading, and performance reporting."
        ),
        institution_context="Academic and Corporate Training Environment",
        primary_users=["Student"],
        secondary_users=["Instructor", "Administrator"],
        actors=["Student", "Instructor", "Administrator"],
        actors_with_responsibilities={
            "Student": "Browse available courses, enroll in course modules, view lessons, submit quizzes/assignments, view grades.",
            "Instructor": "Create courses, upload lessons, publish quizzes, grade student submissions, view course metrics.",
            "Administrator": "Manage student/instructor accounts, resolve enrollment issues, view aggregate reporting logs.",
        },
        domain_problems=[
            "Manual student grading processes are slow and error-prone.",
            "Course enrollment tracking is disorganized.",
            "Lack of real-time student course progress statistics.",
            "Difficulty distributing assignments and resources.",
        ],
        business_goals=[
            "Establish a centralized course repository.",
            "Provide automated course enrollment and progress tracking.",
            "Allow instructors to grade assignments electronically.",
            "Generate detailed student learning metrics.",
        ],
        measurable_success_criteria=[
            "Course lesson page load latency is under 200ms.",
            "Enrollment status updates automatically upon student course sign-up.",
            "99.9% successful submission rate for quizzes and assignments.",
            "Instructor dashboard shows real-time course completions.",
        ],
        entities=[
            "User Profile",
            "Student Profile",
            "Instructor Profile",
            "Course",
            "Lesson Module",
            "Enrollment Record",
            "Quiz Submission",
            "Assignment Grade",
            "Course Analytics",
        ],
        workflows=[
            "Register student profile",
            "Enroll in course",
            "View lesson details",
            "Submit quiz assignment",
            "Grade student work",
            "View course progress analytics",
        ],
        modules=[
            "Authentication and Role Management",
            "Course Catalog Management",
            "Student Enrollment Service",
            "Lesson Delivery Service",
            "Quiz and Assignment Submission",
            "Grading and Feedback Management",
            "Analytics and Student Reporting",
        ],
        business_rules=[
            "Students can only view lessons of courses they are enrolled in.",
            "Only instructors can create course materials and enter grades.",
            "Quizzes must be submitted before the course deadline expires.",
            "Course completions require all lesson steps to be marked as done.",
        ],
        functional_requirements=[
            "FR-001 Student Registrations and Portals",
            "FR-002 Course Catalog and Details",
            "FR-003 Student Enrollments",
            "FR-004 Lesson Delivery",
            "FR-005 Quiz and Assignment Submissions",
            "FR-006 Electronic Grading",
            "FR-007 Course Progress Tracking",
            "FR-008 Course Analytics Dashboard",
        ],
        non_functional_requirements=[
            "Lesson page latency under 200ms for p95 requests.",
            "Enrollment state consistency across student profiles.",
            "Reliable backup of quiz and grade submissions.",
            "Uptime of learning portals during school terms (99.9%).",
            "Secure storage of student records.",
        ],
        feasibility_points={
            "technical": "Highly feasible. Lesson media delivery uses content delivery networks. Grade databases are locked for student security. Quizzes use standard forms.",
            "operational": "Speeds grading tasks and automates student enrollment records. Minimal training is needed for instructors.",
            "economic": "Extremely cost-effective. Eliminates paper resources, reduces staff effort, and scales within standard budgets.",
            "schedule": "Feasible for 6-week completion. Phase 1: Courses & RBAC (Weeks 1-2). Phase 2: Enrollment & Lessons (Weeks 3-4). Phase 3: Quizzes & Grading (Weeks 5-6).",
            "legal": "Compliant with student record privacy regulations (FERPA).",
        },
        api_resources=[
            "/api/v1/auth/register",
            "/api/v1/auth/token",
            "/api/v1/courses",
            "/api/v1/enrollments",
            "/api/v1/lessons",
            "/api/v1/submissions",
            "/api/v1/grades",
        ],
        database_tables=[
            "users",
            "roles",
            "students",
            "instructors",
            "courses",
            "lessons",
            "enrollments",
            "submissions",
            "grades",
        ],
        reports=[
            "Student Course Performance Report",
            "Course Completion Metrics",
            "Instructor Grading Statistics",
            "Active Enrollments Audit Ledger",
        ],
        risks=[
            "System offline during student exam window.",
            "Loss of student assignment submission uploads.",
            "Unauthorized grade alteration.",
        ],
        assumptions=[
            "Students have internet access.",
            "Instructors upload resources in standard formats.",
        ],
        constraints=[
            "Must support common modern web browsers.",
            "Uptime must meet school term SLAs.",
        ],
        out_of_scope=[
            "Physical campus classroom booking.",
            "Tuition fee financial transactions.",
        ],
        validation_rules=[
            "Course Validation: Course title and instructor ID are required.",
            "Enrollment Validation: Student must not be already enrolled.",
            "Submission Validation: Submission file must be present.",
        ],
        edge_cases=[
            "EC-001: Video player fails due to slow student connection. (Mitigation: Quality fallback)",
            "EC-002: Concurrent quiz submission at deadline. (Mitigation: PostgreSQL row locking)",
        ],
        request_response_examples="""### Enroll In Course (POST `/api/v1/enrollments`)
- **Request Payload**:
```json
{
  "course_id": "c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
  "student_id": "b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22"
}
```
- **Response Payload (HTTP 201 Created)**:
```json
{
  "id": "e98fb91f-0b0c-4e8b-a25e-e099bc11a43a",
  "status": "enrolled",
  "created_at": "2026-06-30T00:00:00Z"
}
```""",
        authorization_matrix="""| Role | View Lessons | Submit Quizzes | Edit Syllabus | Grade Submissions |
|------|---|---|---|---|
| Student | Yes | Yes | No | No |
| Instructor | Yes | No | Yes | Yes |
| Administrator | Yes | No | Yes | Yes |""",
        traceability_matrix="""| Req ID | Component / Service | Database Table | Verification Method |
|--------|---------------------|----------------|---------------------|
| FR-003 | Enrollment Service | enrollments | Unit Test |
| FR-004 | Lesson Service | lessons | Integration Test |
| FR-006 | Grading Service | grades | Unit Test |""",
    ),
    "inventory-management": DomainContext(
        project_name="Inventory Management System",
        normalized_domain="inventory-management",
        domain_summary=(
            "The Inventory Management System tracks warehouse stock levels, "
            "supplier products, purchase orders, reorder point thresholds, and stock transfers."
        ),
        institution_context="Warehouse and Supply Chain Environment",
        primary_users=["Warehouse Staff"],
        secondary_users=["Inventory Manager", "Supplier Admin"],
        actors=["Warehouse Staff", "Inventory Manager", "Supplier Admin"],
        actors_with_responsibilities={
            "Warehouse Staff": "Scan item barcodes, update stock counts, dispatch items, verify shipments, report physical counts.",
            "Inventory Manager": "Monitor stock thresholds, create purchase orders, approve suppliers, review warehouse reports.",
            "Supplier Admin": "Receive purchase orders, update shipping dates, verify item details.",
        },
        domain_problems=[
            "Stock counts are inaccurate due to manual errors.",
            "Delay in ordering items when stock is low.",
            "Disorganized warehouse space and slow picking rates.",
            "Lack of visibility into purchase order fulfillment.",
        ],
        business_goals=[
            "Establish real-time visibility into inventory stock counts.",
            "Automate purchase order generation when stock falls below reorder points.",
            "Support barcode scanners for quick warehousing operations.",
            "Coordinate supplier delivery schedules.",
        ],
        measurable_success_criteria=[
            "Stock check query response times stay below 200ms.",
            "Zero discrepancies between physical scans and system counts.",
            "Purchase orders auto-generate immediately when reorder points trigger.",
            "Dispatch logs are updated automatically upon shipment creation.",
        ],
        entities=[
            "SKU Item Record",
            "Warehouse Location",
            "Stock Count Log",
            "Supplier Profile",
            "Purchase Order",
            "PO Item Details",
            "Dispatch Record",
            "Reorder Threshold Policy",
        ],
        workflows=[
            "Update stock item counts",
            "Scan item barcode",
            "Check reorder thresholds",
            "Generate purchase order",
            "Process supplier shipment",
            "Fulfill warehouse dispatch",
        ],
        modules=[
            "Authentication and Role Management",
            "Stock Item Registry",
            "Warehouse Location Tracking",
            "Circulation and Stock Movement",
            "Purchase Order Processing",
            "Supplier and Vendor Management",
            "Inventory Reporting and Analytics",
        ],
        business_rules=[
            "Stock items must have a unique SKU identifier.",
            "Purchase orders require manager approval if amount exceeds limit.",
            "Reorder triggers automatically send alerts to supplier managers.",
            "Stock counts cannot go below zero.",
            "Only inventory managers can update reorder thresholds.",
        ],
        functional_requirements=[
            "FR-001 Stock Item Registry",
            "FR-002 Barcode Scanning",
            "FR-003 Stock Levels Tracking",
            "FR-004 Reorder Point Thresholds",
            "FR-005 Auto Purchase Orders",
            "FR-006 Supplier Profiles",
            "FR-007 Warehouse Location Tracking",
            "FR-008 Stock Transfers",
            "FR-009 Shipment Dispatch Records",
            "FR-010 Stock Reports",
        ],
        non_functional_requirements=[
            "Stock count query latency under 200ms for p95 requests.",
            "Stock transaction consistency (prevent race conditions).",
            "Security logs for all inventory adjustments.",
            "High availability for warehouse scanners (99.9% uptime).",
            "Database durability to protect inventory ledgers.",
        ],
        feasibility_points={
            "technical": "Highly feasible. Barcode scanners use standard serial inputs. Stock transactions use strict serial isolation levels in SQL database.",
            "operational": "Replaces manual checklists, reducing stock errors. Minimal training is needed for staff.",
            "economic": "Extremely viable. Prevents inventory loss and delays. Uptime fits standard budgets.",
            "schedule": "Feasible for 6-week completion. Phase 1: Stock Registry (Weeks 1-2). Phase 2: Barcode & Reorder Point (Weeks 3-4). Phase 3: POs & Suppliers (Weeks 5-6).",
            "legal": "Ensures audit trails for tax and financial record-keeping.",
        },
        api_resources=[
            "/api/v1/auth/register",
            "/api/v1/auth/token",
            "/api/v1/items",
            "/api/v1/stock",
            "/api/v1/purchase-orders",
            "/api/v1/suppliers",
            "/api/v1/dispatch",
        ],
        database_tables=[
            "users",
            "roles",
            "items",
            "suppliers",
            "purchase_orders",
            "po_items",
            "stock_logs",
            "warehouses",
            "dispatches",
        ],
        reports=[
            "Low Stock Valuation Report",
            "Supplier Lead Time Performance",
            "Warehouse Storage Utilization",
            "Stock Movement Ledger",
        ],
        risks=[
            "Incorrect inventory counts due to unrecorded stock movements.",
            "Out-of-stock items due to delayed supplier deliveries.",
            "Unauthorized stock adjustments.",
        ],
        assumptions=[
            "Staff have barcode scanning devices.",
            "Suppliers have email accounts.",
        ],
        constraints=[
            "Must support low-bandwidth warehouse environments.",
            "Uptime must meet warehouse operational shifts.",
        ],
        out_of_scope=[
            "Physical vehicle fleet scheduling.",
            "Warehouse facility temperature controls.",
        ],
        validation_rules=[
            "SKU Validation: SKU code must match standard format.",
            "Stock Validation: Quantity must be non-negative.",
            "Purchase Order Validation: Vendor must be active.",
        ],
        edge_cases=[
            "EC-001: Concurrent inventory updates. (Mitigation: Database transaction locks)",
            "EC-002: Supplier cancels purchase order. (Mitigation: Rollback stock projection status)",
        ],
        request_response_examples="""### Update Stock (POST `/api/v1/stock`)
- **Request Payload**:
```json
{
  "item_id": "c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
  "quantity_adjustment": 50,
  "reason": "Restock shipment"
}
```
- **Response Payload (HTTP 200 OK)**:
```json
{
  "id": "e98fb91f-0b0c-4e8b-a25e-e099bc11a43a",
  "current_stock": 150,
  "last_updated": "2026-06-30T00:00:00Z"
}
```""",
        authorization_matrix="""| Role | Scan Stock | View Inventory | Edit Reorder Limit | Create Vendor |
|------|---|---|---|---|
| Dispatcher | Yes | Yes | No | No |
| Inventory Manager | Yes | Yes | Yes | Yes |
| Supplier Admin | No | Yes | No | No |""",
        traceability_matrix="""| Req ID | Component / Service | Database Table | Verification Method |
|--------|---------------------|----------------|---------------------|
| FR-001 | Item Service | items | Unit Test |
| FR-003 | Stock Service | stock_logs | Unit Test |
| FR-005 | PO Service | purchase_orders| Integration Test |""",
    ),
    "task-management": DomainContext(
        project_name="Task Management System",
        normalized_domain="task-management",
        domain_summary=(
            "The Task Management System tracks project sprints, board columns, "
            "task priority states, assignees, deadlines, and task completions."
        ),
        institution_context="Project Development Environment",
        primary_users=["Developer"],
        secondary_users=["Project Manager", "System Admin"],
        actors=["Developer", "Project Manager", "System Admin"],
        actors_with_responsibilities={
            "Developer": "Create tasks, update status columns, assign tasks to self, log progress notes.",
            "Project Manager": "Create project sprints, assign tasks, view progress boards, generate burndown charts.",
            "System Admin": "Manage system configurations, user accounts, and security audit logs.",
        },
        domain_problems=[
            "Lack of visibility into project sprint progress.",
            "Disorganized tasks and missed deadlines.",
            "Bottlenecks due to unequal task distribution.",
        ],
        business_goals=[
            "Establish real-time project progress boards.",
            "Provide task tracking with deadline notifications.",
            "Coordinate sprint planning and reports.",
        ],
        measurable_success_criteria=[
            "Board update transaction times stay below 200ms.",
            "Zero tasks left without clear status columns.",
            "Daily sprint reports compile accurately.",
        ],
        entities=[
            "User Profile",
            "Project Sprint",
            "Board Column",
            "Task Item",
            "Task Assignee",
            "Progress Comment",
            "Sprint Report",
        ],
        workflows=[
            "Create task item",
            "Assign task to developer",
            "Update board column status",
            "Create project sprint",
            "Generate sprint progress report",
        ],
        modules=[
            "Authentication and Role Management",
            "Sprint Management",
            "Board Columns Service",
            "Task CRUD Operations",
            "Task Status Updates",
            "Reporting Dashboard",
        ],
        business_rules=[
            "Tasks must belong to a valid board column.",
            "Only project managers can create sprints.",
            "Developers can only modify status on assigned tasks.",
        ],
        functional_requirements=[
            "FR-001 Developer Portals",
            "FR-002 Project Sprints",
            "FR-003 Task CRUD Operations",
            "FR-004 Task Status Updates",
            "FR-005 Deadlines Alerts",
            "FR-006 Progress Comments",
            "FR-007 Sprint Progress Reports",
        ],
        non_functional_requirements=[
            "Board update latency under 200ms for p95 requests.",
            "Consistency of task states across sprint boards.",
            "High availability of project portals (99.9% uptime).",
        ],
        feasibility_points={
            "technical": "Highly feasible. Task boards use standard database relations. Updates are checked using transaction isolation.",
            "operational": "Replaces manual spreadsheets with real-time sprint boards. Minimal training is required.",
            "economic": "Extremely cost-effective. Uses open-source stack to fit small-scale budgets.",
            "schedule": "Feasible for 4-week completion.",
            "legal": "No complex compliance rules beyond user access audit logs.",
        },
        api_resources=[
            "/api/v1/auth/register",
            "/api/v1/auth/token",
            "/api/v1/sprints",
            "/api/v1/tasks",
            "/api/v1/boards",
        ],
        database_tables=[
            "users",
            "roles",
            "sprints",
            "tasks",
            "columns",
            "comments",
        ],
        reports=[
            "Sprint Burndown Chart",
            "Developer Workload Stats",
            "Task Cycle Time Analysis",
        ],
        risks=[
            "Failed task state synchronizations.",
            "Loss of sprint board comments.",
        ],
        assumptions=[
            "Developers have internet terminals.",
        ],
        constraints=[
            "Must support concurrent updates on sprint boards.",
        ],
        out_of_scope=[
            "Direct calendar schedule booking.",
            "Financial resource accounting.",
        ],
        validation_rules=[
            "Task Validation: Task title must be present.",
            "Sprint Validation: Start and end dates must be valid.",
        ],
        edge_cases=[
            "EC-001: Concurrent updates on the same task. (Mitigation: PostgreSQL row locking)",
        ],
        request_response_examples="""### Update Task (POST `/api/v1/tasks`)
- **Request Payload**:
```json
{
  "title": "Fix database transaction",
  "sprint_id": "c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
  "status": "in_progress"
}
```
- **Response Payload (HTTP 200 OK)**:
```json
{
  "id": "e98fb91f-0b0c-4e8b-a25e-e099bc11a43a",
  "status": "in_progress",
  "last_updated": "2026-06-30T00:00:00Z"
}
```""",
        authorization_matrix="""| Role | Create Task | Update Status | Edit Sprint | Manage Users |
|------|---|---|---|---|
| Developer | Yes | Yes (Assigned) | No | No |
| Project Manager | Yes | Yes | Yes | No |
| System Admin | Yes | Yes | Yes | Yes |""",
        traceability_matrix="""| Req ID | Component / Service | Database Table | Verification Method |
|--------|---------------------|----------------|---------------------|
| FR-003 | Task Service | tasks | Unit Test |
| FR-004 | Board Service | columns | Unit Test |""",
    ),
    "generic-business-app": DomainContext(
        project_name="Business Management System",
        normalized_domain="generic-business-app",
        domain_summary=(
            "The Business Management System coordinates user accounts, business resource logs, "
            "reporting directories, and system audit logs."
        ),
        institution_context="General Business Operation Environment",
        primary_users=["Staff User"],
        secondary_users=["Manager", "Administrator"],
        actors=["Staff User", "Manager", "Administrator"],
        actors_with_responsibilities={
            "Staff User": "Register account, browse business catalog, create business records, update progress details.",
            "Manager": "Monitor business performance, approve adjustments, request reporting files.",
            "Administrator": "Manage system configurations, user accounts, policies, and audit logs.",
        },
        domain_problems=[
            "Inaccuracies in manual business logs.",
            "Slow data indexing and report compilation.",
            "Lack of visibility into active resource utilization.",
        ],
        business_goals=[
            "Establish a centralized business database.",
            "Provide automated audit tracking for business records.",
            "Enforce security policy access controls.",
        ],
        measurable_success_criteria=[
            "Catalog search responses stay under 300ms.",
            "100% of resource updates are logged in compliance audit trails.",
            "Dashboard metrics reflect updates in real-time.",
        ],
        entities=[
            "User Profile",
            "Role Profile",
            "Resource Record",
            "Business Log",
            "Approval Decision",
            "Audit Trail",
        ],
        workflows=[
            "Register user account",
            "Add business resource",
            "Search business records",
            "Approve record changes",
            "Generate business report",
        ],
        modules=[
            "Authentication and Role Management",
            "Business Catalog Management",
            "Resource Tracking Service",
            "Approval Operations",
            "Reporting Dashboard",
            "System Audit Logs",
        ],
        business_rules=[
            "Business resources must have a unique identifier.",
            "Modifications to sensitive records require manager approval.",
            "User access is strictly restricted by assigned roles.",
        ],
        functional_requirements=[
            "FR-001 User Registrations",
            "FR-002 Business Catalog",
            "FR-003 Resource Tracking",
            "FR-004 Record Approvals",
            "FR-005 Daily Reports",
            "FR-006 System Audit Logs",
        ],
        non_functional_requirements=[
            "Search query response time under 300ms for p95 requests.",
            "Data transaction consistency and reliability.",
            "Encryption of sensitive user information.",
        ],
        feasibility_points={
            "technical": "Highly feasible. Relational database holds records. Standard API routing distributes actions.",
            "operational": "Replaces manual record logs. Requires basic training for staff.",
            "economic": "Extremely cost-effective. Fits standard virtual server budgets.",
            "schedule": "Feasible for 4-week completion.",
            "legal": "Audit logging provides compliance security.",
        },
        api_resources=[
            "/api/v1/auth/register",
            "/api/v1/auth/token",
            "/api/v1/resources",
            "/api/v1/approvals",
            "/api/v1/audit",
        ],
        database_tables=[
            "users",
            "roles",
            "resources",
            "approvals",
            "audit_logs",
        ],
        reports=[
            "Daily Resource Utilization",
            "System Audit Trails",
            "Weekly Progress Summary",
        ],
        risks=[
            "Loss of physical resource records.",
            "Slow report creation due to database lockups.",
        ],
        assumptions=[
            "Users have internet terminal access.",
        ],
        constraints=[
            "Must support common modern web browsers.",
        ],
        out_of_scope=[
            "Custom external payroll processing.",
        ],
        validation_rules=[
            "Resource Validation: Resource title is required.",
        ],
        edge_cases=[
            "EC-001: Deleting critical system configuration. (Mitigation: Require Admin confirmation)",
        ],
        request_response_examples="""### Create Resource (POST `/api/v1/resources`)
- **Request Payload**:
```json
{
  "title": "Business ledger Q2",
  "category": "Finance"
}
```
- **Response Payload (HTTP 201 Created)**:
```json
{
  "id": "e98fb91f-0b0c-4e8b-a25e-e099bc11a43a",
  "status": "created",
  "created_at": "2026-06-30T00:00:00Z"
}
```""",
        authorization_matrix="""| Role | View Records | Create Records | Approve Changes | Edit Settings |
|------|---|---|---|---|
| Standard | Yes | Yes | No | No |
| Manager | Yes | Yes | Yes | No |
| Administrator | Yes | Yes | Yes | Yes |""",
        traceability_matrix="""| Req ID | Component / Service | Database Table | Verification Method |
|--------|---------------------|----------------|---------------------|
| FR-003 | Resource Service | resources | Unit Test |
| FR-006 | Audit Service | audit_logs | Unit Test |""",
    ),
}
