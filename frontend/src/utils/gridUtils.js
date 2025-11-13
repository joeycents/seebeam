/**
 * Utility functions for generating and randomizing grid points
 * As per RealEye whitepaper specifications
 */

/**
 * Generate 13-point grid for desktop (Re-Validation task)
 * Layout: 5 points top row, 5 points middle row, 3 points bottom row
 */
export function generate13PointGrid(screenWidth, screenHeight) {
  const w = screenWidth;
  const h = screenHeight;
  const margin = { x: w * 0.1, y: h * 0.1 };

  const positions = [];

  // Top row (5 points)
  const y1 = margin.y;
  for (let i = 0; i < 5; i++) {
    const x = margin.x + (w - 2 * margin.x) * i / 4;
    positions.push({ x, y: y1 });
  }

  // Middle row (5 points)
  const y2 = h / 2;
  for (let i = 0; i < 5; i++) {
    const x = margin.x + (w - 2 * margin.x) * i / 4;
    positions.push({ x, y: y2 });
  }

  // Bottom row (3 points - left, center, right)
  const y3 = h - margin.y;
  [0, 2, 4].forEach(i => {
    const x = margin.x + (w - 2 * margin.x) * i / 4;
    positions.push({ x, y: y3 });
  });

  return positions;
}

/**
 * Generate 49-point grid for desktop (Large Grid task)
 * Layout: 7×7 grid
 */
export function generate49PointGrid(screenWidth, screenHeight) {
  const w = screenWidth;
  const h = screenHeight;
  const margin = { x: w * 0.05, y: h * 0.05 };

  const positions = [];

  for (let row = 0; row < 7; row++) {
    const y = margin.y + (h - 2 * margin.y) * row / 6;
    for (let col = 0; col < 7; col++) {
      const x = margin.x + (w - 2 * margin.x) * col / 6;
      positions.push({ x, y });
    }
  }

  return positions;
}

/**
 * Randomize array order, starting from center position
 * As per whitepaper: "random order, starting from center"
 */
export function randomizeFromCenter(positions) {
  if (positions.length === 0) return [];

  // Find center position (middle of the array for 13-point, actual center for grids)
  const centerIndex = Math.floor(positions.length / 2);

  // Separate center from rest
  const center = positions[centerIndex];
  const remaining = positions.filter((_, idx) => idx !== centerIndex);

  // Fisher-Yates shuffle for remaining positions
  const shuffled = [...remaining];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }

  // Return with center first
  return [center, ...shuffled];
}

/**
 * Calculate Euclidean distance between two points
 */
export function calculateDistance(p1, p2) {
  if (!p1 || !p2) return Infinity;
  const dx = p1.x - p2.x;
  const dy = p1.y - p2.y;
  return Math.sqrt(dx * dx + dy * dy);
}
