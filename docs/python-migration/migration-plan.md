# Java to Python Migration Plan

## Project Overview

| Item | Value |
|------|-------|
| Source Project | cp-mes-ruoyi (Java/Spring Boot) |
| Target Stack | Python 3.11+ / Django 5.0 / PostgreSQL 16 |
| Source Code Scale | 570 Java files, 43,107 lines |
| Database Tables | 39 tables |
| API Endpoints | ~300+ |

---

## 1. Technology Stack Mapping

### Core Framework

| Java | Python (Django) |
|------|-----------------|
| Spring Boot 2.7.9 | Django 5.0 |
| Spring MVC | Django REST Framework |
| Spring Security | Django REST Framework + JWT |
| Spring IoC/DI | Django built-in |

### Data Layer

| Java | Python |
|------|--------|
| MyBatis-Plus 3.5.3.1 | Django ORM |
| HikariCP | psycopg3 connection pooling |
| P6Spy | django-debug-toolbar |
| Dynamic Datasource | django-tenants (multi-tenant) |

### Authentication & Authorization

| Java | Python |
|------|--------|
| Sa-Token 1.34.0 | djangorestframework-simplejwt |
| JWT Token | PyJWT |
| Permission Annotations | DRF permission classes |

### Caching

| Java | Python |
|------|--------|
| Redisson 3.20.0 | django-redis |
| Spring Cache | Django cache framework |

### Task Scheduling

| Java | Python |
|------|--------|
| XXL-Job 2.3.1 | Celery + Redis |
| Spring @Scheduled | Celery Beat |

### File Storage

| Java | Python |
|------|--------|
| MinIO/S3 SDK | boto3 / django-storages |
| Local Storage | Django FileSystemStorage |

### Excel Processing

| Java | Python |
|------|--------|
| EasyExcel 3.2.1 | openpyxl / pandas |
| Excel Annotations | django-import-export |

### Utilities

| Java | Python |
|------|--------|
| Hutool 5.8.15 | Python stdlib + pydantic |
| MapStruct | pydantic / dataclasses |
| Jackson | orjson / pydantic |

---

## 2. Migration Phases

### Phase 1: Project Setup & Infrastructure (Week 1-2)

**Objectives:**
- Initialize Django project structure
- Configure PostgreSQL database
- Set up development environment
- Configure Redis caching
- Set up Celery for task scheduling

**Deliverables:**
- Django project skeleton
- Docker development environment
- Database connection configured
- Redis cache configured
- Basic logging setup

**Tasks:**
1. Create Django project with proper app structure
2. Configure PostgreSQL with psycopg3
3. Set up django-redis for caching
4. Configure Celery with Redis broker
5. Create Docker Compose for local development
6. Set up pytest and test infrastructure
7. Configure django-cors-headers for API access

---

### Phase 2: Database Migration (Week 3-4)

**Objectives:**
- Convert all 39 database tables to Django models
- Create database migrations
- Set up multi-tenancy support
- Implement data permission layer

**Deliverables:**
- Complete Django models for all tables
- Database migrations ready
- Multi-tenant schema support
- Row-level permission system

**Tasks:**
1. Analyze existing MySQL schema
2. Create Django models mapping
3. Convert to PostgreSQL data types
4. Implement django-tenants for multi-tenancy
5. Create custom managers for data permission
6. Add database indexes and constraints
7. Create initial data fixtures

---

### Phase 3: Authentication & Authorization (Week 5-6)

**Objectives:**
- Implement JWT authentication
- Migrate user/role/permission system
- Implement data scope permissions

**Deliverables:**
- JWT authentication system
- User, Role, Menu, Dept models and APIs
- Permission decorators
- Data scope filtering

**Tasks:**
1. Implement JWT token generation/validation
2. Create custom authentication backend
3. Migrate user management APIs
4. Migrate role and permission APIs
5. Implement menu and dept APIs
6. Create permission decorators (替代 @SaCheckPermission)
7. Implement data scope filtering (替代 @DataPermission)

---

### Phase 4: Core System APIs (Week 7-10)

**Objectives:**
- Migrate all system management APIs
- Implement logging and monitoring

**Deliverables:**
- Complete system management APIs
- Operation logging system
- Online user monitoring

**Tasks:**
1. Migrate dict management APIs
2. Migrate config management APIs
3. Migrate post management APIs
4. Migrate login log APIs
5. Migrate operation log APIs
6. Implement online user tracking
7. Create cache management APIs

---

### Phase 5: Business Module - Basic Data (Week 11-12)

**Objectives:**
- Migrate basic data management module

**Deliverables:**
- Client management APIs
- Product management APIs
- Procedure management APIs
- Process route management APIs
- Defect management APIs

**Tasks:**
1. Migrate client (客户) APIs
2. Migrate product (产品) APIs
3. Migrate procedure (工序) APIs
4. Migrate process route (工艺路线) APIs
5. Migrate defect (不良项) APIs

---

### Phase 6: Business Module - Production (Week 13-15)

**Objectives:**
- Migrate production management module

**Deliverables:**
- Work order (工单) APIs
- Task management APIs
- Job booking (报工) APIs
- Production statistics APIs

**Tasks:**
1. Migrate sheet (工单) APIs
2. Migrate task (任务) APIs
3. Migrate job booking (报工) APIs
4. Implement production statistics
5. Create production reports

---

### Phase 7: Business Module - Inventory (Week 16-17)

**Objectives:**
- Migrate inventory management module

**Deliverables:**
- Material management APIs
- Supplier management APIs
- Stock in/out APIs
- Inventory statistics

**Tasks:**
1. Migrate material (物料) APIs
2. Migrate supplier (供应商) APIs
3. Migrate stock operations APIs
4. Implement inventory statistics

---

### Phase 8: Advanced Features (Week 18-20)

**Objectives:**
- Migrate advanced features

**Deliverables:**
- Excel import/export
- Custom fields
- Custom reports
- Scheduled tasks

**Tasks:**
1. Implement Excel import/export with django-import-export
2. Migrate custom field functionality
3. Migrate custom report functionality
4. Convert XXL-Job tasks to Celery tasks
5. Implement rate limiting
6. Implement repeat submit prevention

---

### Phase 9: Frontend Integration (Week 21-22)

**Objectives:**
- Update frontend to work with new backend

**Deliverables:**
- Updated API endpoints
- Frontend configuration updated
- Integration testing

**Tasks:**
1. Update API endpoint paths
2. Update authentication flow
3. Fix any breaking changes
4. Perform integration testing

---

### Phase 10: Testing & Deployment (Week 23-25)

**Objectives:**
- Complete testing
- Production deployment setup

**Deliverables:**
- Test coverage > 80%
- Production deployment guide
- Monitoring setup

**Tasks:**
1. Write unit tests
2. Write integration tests
3. Performance testing
4. Create production Docker images
5. Set up Nginx configuration
6. Configure monitoring (Prometheus/Grafana)
7. Create deployment documentation

---

## 3. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Multi-tenancy complexity | High | Use django-tenants library, thorough testing |
| Data permission logic | High | Create comprehensive test cases, code review |
| Business logic in XML mappers | Medium | Careful code review, pair programming |
| Encryption compatibility | Medium | Use same algorithms, verify with test data |
| API compatibility | Medium | Maintain same endpoint paths, version APIs |
| Performance regression | Medium | Benchmark critical paths, optimize queries |

---

## 4. Team Structure

| Role | Count | Responsibilities |
|------|-------|------------------|
| Tech Lead | 1 | Architecture, code review, technical decisions |
| Backend Developer | 2 | API development, business logic |
| Database Engineer | 1 | Database migration, optimization |
| QA Engineer | 1 | Testing, quality assurance |

---

## 5. Milestones

| Milestone | Week | Deliverable |
|-----------|------|-------------|
| M1: Infrastructure Ready | Week 2 | Django project running with DB |
| M2: Auth System Complete | Week 6 | User can login and access APIs |
| M3: System APIs Complete | Week 10 | All system management APIs working |
| M4: Basic Data Complete | Week 12 | Basic data module fully migrated |
| M5: Production Complete | Week 15 | Production module fully migrated |
| M6: All Features Complete | Week 20 | All features migrated |
| M7: Integration Complete | Week 22 | Frontend working with new backend |
| M8: Production Ready | Week 25 | Deployed and tested |

---

## 6. Success Criteria

1. All 300+ API endpoints migrated and functional
2. All 39 database tables migrated
3. Multi-tenancy working correctly
4. Data permission working correctly
5. Test coverage > 80%
6. Performance within 10% of original system
7. Frontend fully functional with new backend
8. Documentation complete
