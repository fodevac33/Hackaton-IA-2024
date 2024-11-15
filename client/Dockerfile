# Use an official Node.js image
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# Move necessary files from `node_modules` to the `dist` directory
RUN cp node_modules/@ricky0123/vad-web/dist/silero_vad.onnx dist/ && \
    cp node_modules/@ricky0123/vad-web/dist/vad.worklet.bundle.min.js dist/ && \
    cp node_modules/onnxruntime-web/dist/ort-wasm-simd-threaded.mjs dist/ && \
    cp node_modules/onnxruntime-web/dist/*.wasm dist/

# Expose the port Vite will use for preview
EXPOSE 4173

# Serve the application using `vite preview`
CMD ["npm", "run", "preview"]
