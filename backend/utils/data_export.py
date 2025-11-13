"""
Data Export Module
Handles formatting and exporting gaze tracking data
"""
import json
import csv
from typing import List, Dict, Any
from datetime import datetime
import os


class DataExporter:
    """
    Exports gaze tracking data in various formats
    """

    def __init__(self):
        """
        Initialize data exporter
        """
        self.session_data = []

    def add_gaze_point(self,
                      timestamp: float,
                      gaze_x: float,
                      gaze_y: float,
                      fixation: bool = False,
                      fixation_id: str = None,
                      confidence: float = 1.0,
                      metadata: Dict = None):
        """
        Add a gaze point to the session

        Args:
            timestamp: Timestamp in milliseconds
            gaze_x: Gaze X coordinate (percentage)
            gaze_y: Gaze Y coordinate (percentage)
            fixation: Whether this is part of a fixation
            fixation_id: Fixation ID if applicable
            confidence: Confidence score
            metadata: Additional metadata
        """
        data_point = {
            "timestamp": timestamp,
            "gazePointX": gaze_x,
            "gazePointY": gaze_y,
            "fixation": fixation,
            "fixationId": fixation_id,
            "confidence": confidence
        }

        if metadata:
            data_point["metadata"] = metadata

        self.session_data.append(data_point)

    def export_json(self, filepath: str, pretty: bool = True):
        """
        Export data as JSON

        Args:
            filepath: Output file path
            pretty: Use pretty printing
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w') as f:
            if pretty:
                json.dump(self.session_data, f, indent=2)
            else:
                json.dump(self.session_data, f)

        print(f"✓ Exported {len(self.session_data)} points to {filepath}")

    def export_csv(self, filepath: str):
        """
        Export data as CSV

        Args:
            filepath: Output file path
        """
        if len(self.session_data) == 0:
            print("No data to export")
            return

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Get all keys from first data point (excluding metadata)
        keys = [k for k in self.session_data[0].keys() if k != 'metadata']

        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()

            for point in self.session_data:
                row = {k: point[k] for k in keys}
                writer.writerow(row)

        print(f"✓ Exported {len(self.session_data)} points to {filepath}")

    def export_realeye_format(self, filepath: str):
        """
        Export in RealEye-compatible format

        Args:
            filepath: Output file path
        """
        self.export_json(filepath, pretty=True)

    def get_summary_statistics(self) -> Dict:
        """
        Get summary statistics for the session

        Returns:
            Dictionary with statistics
        """
        if len(self.session_data) == 0:
            return {'total_points': 0}

        fixations = [p for p in self.session_data if p['fixation']]
        unique_fixations = len(set(p['fixationId'] for p in fixations if p['fixationId']))

        timestamps = [p['timestamp'] for p in self.session_data]
        duration = max(timestamps) - min(timestamps) if timestamps else 0

        return {
            'total_points': len(self.session_data),
            'total_fixations': unique_fixations,
            'duration_ms': duration,
            'fixation_percentage': (len(fixations) / len(self.session_data) * 100) if self.session_data else 0,
            'mean_confidence': sum(p['confidence'] for p in self.session_data) / len(self.session_data)
        }

    def generate_heatmap_data(self, grid_size: int = 50) -> List[List[float]]:
        """
        Generate heatmap data for visualization

        Args:
            grid_size: Size of heatmap grid (grid_size × grid_size)

        Returns:
            2D array with gaze density
        """
        # Initialize grid
        heatmap = [[0.0 for _ in range(grid_size)] for _ in range(grid_size)]

        # Accumulate gaze points
        for point in self.session_data:
            x_pct = point['gazePointX']
            y_pct = point['gazePointY']

            # Convert to grid coordinates
            grid_x = int((x_pct / 100.0) * (grid_size - 1))
            grid_y = int((y_pct / 100.0) * (grid_size - 1))

            # Clamp to grid bounds
            grid_x = max(0, min(grid_size - 1, grid_x))
            grid_y = max(0, min(grid_size - 1, grid_y))

            heatmap[grid_y][grid_x] += 1

        # Normalize
        max_value = max(max(row) for row in heatmap)
        if max_value > 0:
            heatmap = [[cell / max_value for cell in row] for row in heatmap]

        return heatmap

    def clear_session(self):
        """
        Clear current session data
        """
        self.session_data = []

    def generate_session_report(self) -> str:
        """
        Generate human-readable session report

        Returns:
            Formatted report string
        """
        stats = self.get_summary_statistics()

        report = []
        report.append("=" * 60)
        report.append("GAZE TRACKING SESSION REPORT")
        report.append("=" * 60)
        report.append(f"Total Gaze Points:     {stats['total_points']}")
        report.append(f"Total Fixations:       {stats.get('total_fixations', 0)}")
        report.append(f"Session Duration:      {stats.get('duration_ms', 0):.0f} ms")
        report.append(f"Fixation Percentage:   {stats.get('fixation_percentage', 0):.1f}%")
        report.append(f"Mean Confidence:       {stats.get('mean_confidence', 0):.3f}")
        report.append("=" * 60)

        return "\n".join(report)
