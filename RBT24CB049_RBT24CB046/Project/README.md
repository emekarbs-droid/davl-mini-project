# Bank Management System (MERN Stack)

Professional Banking Management System developed for DBMS Project.

## Project Structure
- `backend/`: Express.js server with MongoDB/Mongoose.
- `frontend/`: React + Vite + Tailwind CSS.

## Getting Started

### Prerequisites
- Node.js (v18+)
- MongoDB Atlas account (or local MongoDB)

### Installation
1. Clone the repository.
2. Install all dependencies from the root:
   ```bash
   npm run install-all
   ```

### Development
To run both backend and frontend concurrently:
```bash
npm run dev
```

### Production / Deployment
To build the frontend and start the backend in production mode:
1. Build frontend:
   ```bash
   npm run build
   ```
2. Start backend (it will serve the built frontend):
   ```bash
   NODE_ENV=production npm start
   ```

## Deployment to GitHub/Render
- Push the entire directory to a single GitHub repository.
- To deploy on Render:
  - Create a Web Service pointing to this repo.
  - Root Directory: `backend` (or use the root scripts).
  - Build Command: `cd ../frontend && npm install && npm run build && cd ../backend && npm install`
  - Start Command: `npm start`
  - Environment Variables: Add `MONGO_URI`, `JWT_SECRET`, and set `NODE_ENV` to `production`.
