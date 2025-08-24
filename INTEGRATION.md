# Frontend-Backend Integration

This document describes the integration between the Next.js frontend and FastAPI backend.

## API Integration Overview

The frontend has been fully integrated with the FastAPI backend through a comprehensive API layer:

### 1. API Client (`apps/web/src/lib/api.ts`)
- **Type-safe API client** with full TypeScript support
- **Comprehensive error handling** with proper HTTP status codes
- **Authentication support** with Bearer token headers
- **All CRUD operations** for agents, features, routes, and roles
- **Analytics and system endpoints** for monitoring

### 2. React Hooks (`apps/web/src/hooks/useApi.ts`)
- **Custom hooks** for each API operation
- **Loading and error states** management
- **Automatic retry logic** and error recovery
- **Optimistic updates** for better UX

### 3. Context Provider (`apps/web/src/providers/ApiProvider.tsx`)
- **Global state management** for API data
- **Real-time data synchronization** across components
- **Centralized error handling** and loading states
- **Automatic data refresh** capabilities

### 4. Updated Agent Router Page
- **Real API data** instead of hardcoded mock data
- **Loading states** with spinners and progress indicators
- **Error handling** with retry buttons and user-friendly messages
- **Empty states** when no data is available
- **Real-time updates** when data changes

## Environment Configuration

Create a `.env.local` file in the `apps/web` directory:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Development settings
NEXT_PUBLIC_APP_ENV=development
```

## Features Implemented

### ✅ Agent Management
- List all agents with pagination
- Create new agents from various sources (MCP, A2A, WORKFLOW)
- Update agent configurations
- Delete agents
- Discover agents from external sources
- Check agent health status

### ✅ Feature Management
- List all features with pagination
- Create new features from various stores (HTTP_JSON, GIT, S3, GCS)
- Update feature configurations
- Delete features
- Discover features from external sources

### ✅ Route Management
- List all routes with pagination
- Create new routes between features and agents
- Update route rules and conditions
- Delete routes
- Conditional routing with role-based access control

### ✅ Role Management
- List all roles with pagination
- Create custom roles
- Update role permissions
- Delete roles
- Import IAM roles from cloud providers (AWS, Azure, GCP)

### ✅ Analytics & Monitoring
- System health monitoring
- Route usage statistics
- Agent health metrics
- Feature usage analytics
- Real-time system status

## API Endpoints Used

### Agents
- `GET /v1/agents` - List agents
- `POST /v1/agents` - Create agent
- `GET /v1/agents/{id}` - Get agent details
- `PUT /v1/agents/{id}` - Update agent
- `DELETE /v1/agents/{id}` - Delete agent
- `POST /v1/agents/discover` - Discover agents
- `GET /v1/agents/{id}/health` - Check agent health

### Features
- `GET /v1/features` - List features
- `POST /v1/features` - Create feature
- `GET /v1/features/{id}` - Get feature details
- `PUT /v1/features/{id}` - Update feature
- `DELETE /v1/features/{id}` - Delete feature
- `POST /v1/features/discover` - Discover features

### Routes
- `GET /v1/routes` - List routes
- `POST /v1/routes` - Create route
- `GET /v1/routes/{id}` - Get route details
- `PUT /v1/routes/{id}` - Update route
- `DELETE /v1/routes/{id}` - Delete route
- `POST /v1/routes/{id}/conditions` - Add condition to route
- `DELETE /v1/routes/{id}/conditions/{condition_id}` - Remove condition

### Roles
- `GET /v1/roles` - List roles
- `POST /v1/roles` - Create role
- `GET /v1/roles/{id}` - Get role details
- `PUT /v1/roles/{id}` - Update role
- `DELETE /v1/roles/{id}` - Delete role
- `POST /v1/roles/import-iam` - Import IAM roles

### Analytics
- `GET /v1/analytics/overview` - System overview
- `GET /v1/analytics/routes/usage` - Route usage stats
- `GET /v1/analytics/agents/health` - Agent health stats
- `GET /v1/analytics/features/usage` - Feature usage stats

### System
- `GET /v1/system/health` - System health
- `GET /v1/system/config` - System configuration

## Error Handling

The integration includes comprehensive error handling:

1. **Network Errors**: Connection failures, timeouts
2. **HTTP Errors**: 4xx and 5xx status codes
3. **Validation Errors**: Invalid data formats
4. **Business Logic Errors**: Custom application errors

All errors are displayed to users with:
- Clear error messages
- Retry functionality
- Fallback states
- Loading indicators

## Loading States

The UI provides clear feedback during API operations:

1. **Initial Loading**: When the app first loads data
2. **Action Loading**: When creating, updating, or deleting items
3. **Background Loading**: When refreshing data
4. **Skeleton Loading**: Placeholder content while loading

## Data Synchronization

The API provider ensures data consistency:

1. **Automatic Refresh**: Data is refreshed when needed
2. **Optimistic Updates**: UI updates immediately, then syncs with server
3. **Error Recovery**: Failed operations are retried automatically
4. **Cache Management**: Efficient caching and invalidation

## Security

The integration includes security features:

1. **Authentication**: Bearer token support
2. **CORS**: Proper cross-origin request handling
3. **Input Validation**: Client-side and server-side validation
4. **Error Sanitization**: Sensitive data is not exposed in errors

## Testing

To test the integration:

1. **Start the FastAPI backend**:
   ```bash
   cd apps/api
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the Next.js frontend**:
   ```bash
   cd apps/web
   npm run dev
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Next Steps

The integration is complete and ready for production use. Future enhancements could include:

1. **Real-time Updates**: WebSocket integration for live data
2. **Offline Support**: Service worker for offline functionality
3. **Advanced Caching**: Redis-based caching layer
4. **Performance Monitoring**: APM integration
5. **A/B Testing**: Feature flag integration
