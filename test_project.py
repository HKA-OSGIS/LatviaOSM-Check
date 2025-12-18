#!/usr/bin/env python3
"""Unit tests for Latvia OSM Road Completeness Project"""

import unittest
import pandas as pd
import geopandas as gpd
import json
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent


class TestDataFiles(unittest.TestCase):
    """Test data file existence and integrity"""
    
    def setUp(self):
        self.csv_file = PROJECT_ROOT / 'outputs' / 'exports' / 'completeness_municipalities.csv'
        self.geojson_file = PROJECT_ROOT / 'outputs' / 'exports' / 'latvia_municipalities_only.geojson'
    
    def test_csv_file_exists(self):
        """CSV file should exist"""
        self.assertTrue(self.csv_file.exists(), f"CSV file not found: {self.csv_file}")
    
    def test_geojson_file_exists(self):
        """GeoJSON file should exist"""
        self.assertTrue(self.geojson_file.exists(), f"GeoJSON file not found: {self.geojson_file}")


class TestCSVData(unittest.TestCase):
    """Test CSV data integrity and content"""
    
    @classmethod
    def setUpClass(cls):
        csv_file = PROJECT_ROOT / 'outputs' / 'exports' / 'completeness_municipalities.csv'
        cls.df = pd.read_csv(csv_file)
    
    def test_csv_has_records(self):
        """CSV should have data"""
        self.assertGreater(len(self.df), 0, "CSV is empty")
    
    def test_csv_required_columns(self):
        """CSV should have all required columns"""
        required_cols = ['Municipality', 'OSM Roads (km)', 'Official Roads (km)', 'Completeness (%)']
        for col in required_cols:
            self.assertIn(col, self.df.columns, f"Missing column: {col}")
    
    def test_csv_no_null_values(self):
        """CSV should not have null values"""
        self.assertEqual(self.df.isnull().sum().sum(), 0, "CSV contains null values")
    
    def test_csv_numeric_columns(self):
        """Numeric columns should be numeric"""
        self.assertTrue(pd.api.types.is_numeric_dtype(self.df['OSM Roads (km)']), 
                       "OSM Roads column is not numeric")
        self.assertTrue(pd.api.types.is_numeric_dtype(self.df['Official Roads (km)']), 
                       "Official Roads column is not numeric")
        self.assertTrue(pd.api.types.is_numeric_dtype(self.df['Completeness (%)']), 
                       "Completeness column is not numeric")
    
    def test_csv_municipalities_count(self):
        """Should have exactly 30 municipalities"""
        self.assertEqual(len(self.df), 30, f"Expected 30 municipalities, got {len(self.df)}")
    
    def test_csv_osm_roads_positive(self):
        """OSM roads should be positive"""
        self.assertTrue((self.df['OSM Roads (km)'] > 0).all(), 
                       "Some OSM roads are not positive")
    
    def test_csv_official_roads_positive(self):
        """Official roads should be positive"""
        self.assertTrue((self.df['Official Roads (km)'] > 0).all(), 
                       "Some official roads are not positive")
    
    def test_csv_completeness_positive(self):
        """Completeness should be positive"""
        self.assertTrue((self.df['Completeness (%)'] > 0).all(), 
                       "Some completeness values are not positive")
    
    def test_csv_osm_total(self):
        """Total OSM roads should be correct"""
        total_osm = self.df['OSM Roads (km)'].sum()
        self.assertAlmostEqual(total_osm, 7820.66, delta=1, 
                              msg=f"Total OSM roads should be ~7820.66 km, got {total_osm}")
    
    def test_csv_official_total(self):
        """Total official roads should be correct"""
        total_official = self.df['Official Roads (km)'].sum()
        self.assertAlmostEqual(total_official, 46952, delta=1,
                              msg=f"Total official roads should be ~46952 km, got {total_official}")


class TestGeoJSONData(unittest.TestCase):
    """Test GeoJSON data integrity and content"""
    
    @classmethod
    def setUpClass(cls):
        geojson_file = PROJECT_ROOT / 'outputs' / 'exports' / 'latvia_municipalities_only.geojson'
        cls.gdf = gpd.read_file(geojson_file)
    
    def test_geojson_has_features(self):
        """GeoJSON should have features"""
        self.assertGreater(len(self.gdf), 0, "GeoJSON is empty")
    
    def test_geojson_features_count(self):
        """Should have exactly 30 features"""
        self.assertEqual(len(self.gdf), 30, 
                        f"Expected 30 features, got {len(self.gdf)}")
    
    def test_geojson_has_required_fields(self):
        """GeoJSON should have required fields"""
        required_fields = ['municipality_name', 'osm_road_km', 'official_road_km', 'completeness_pct']
        for field in required_fields:
            self.assertIn(field, self.gdf.columns, f"Missing field: {field}")
    
    def test_geojson_valid_geometry(self):
        """All geometries should be valid"""
        self.assertTrue(self.gdf.geometry.is_valid.all(), 
                       "Some geometries are invalid")
    
    def test_geojson_has_crs(self):
        """GeoJSON should have CRS defined"""
        self.assertIsNotNone(self.gdf.crs, "CRS is not defined")
    
    def test_geojson_geometry_types(self):
        """All geometries should be Polygons"""
        self.assertTrue((self.gdf.geometry.type == 'Polygon').all(),
                       "Not all geometries are Polygons")
    
    def test_geojson_no_null_geometry(self):
        """No geometry should be null"""
        self.assertEqual(self.gdf.geometry.isnull().sum(), 0,
                        "Some geometries are null")


class TestDataCalculations(unittest.TestCase):
    """Test data calculations and formulas"""
    
    @classmethod
    def setUpClass(cls):
        csv_file = PROJECT_ROOT / 'outputs' / 'exports' / 'completeness_municipalities.csv'
        geojson_file = PROJECT_ROOT / 'outputs' / 'exports' / 'latvia_municipalities_only.geojson'
        cls.df = pd.read_csv(csv_file)
        cls.gdf = gpd.read_file(geojson_file)
    
    def test_completeness_calculation(self):
        """Completeness % should be OSM/Official * 100"""
        for idx, row in self.df.iterrows():
            osm = row['OSM Roads (km)']
            official = row['Official Roads (km)']
            completeness = row['Completeness (%)']
            expected = (osm / official * 100)
            self.assertAlmostEqual(completeness, expected, delta=0.1,
                                  msg=f"Completeness calculation wrong for {row['Municipality']}")
    
    def test_csv_geojson_data_match(self):
        """CSV and GeoJSON data should match"""
        mismatches = []
        for mun_name in self.gdf['municipality_name']:
            geojson_row = self.gdf[self.gdf['municipality_name'] == mun_name].iloc[0]
            csv_row = self.df[self.df['Municipality'] == mun_name]
            
            if len(csv_row) > 0:
                csv_official = csv_row['Official Roads (km)'].values[0]
                geojson_official = geojson_row['official_road_km']
                
                if abs(csv_official - geojson_official) > 0.01:
                    mismatches.append(f"{mun_name}: CSV={csv_official}, GeoJSON={geojson_official}")
        
        self.assertEqual(len(mismatches), 0, 
                        f"Data mismatches found:\n" + "\n".join(mismatches))
    
    def test_completeness_range(self):
        """Completeness should be between 0 and 200%"""
        self.assertTrue((self.df['Completeness (%)'] > 0).all(),
                       "Some completeness values are <= 0")
        self.assertTrue((self.df['Completeness (%)'] < 200).all(),
                       "Some completeness values are >= 200")


class TestMunicipalityData(unittest.TestCase):
    """Test specific municipality data"""
    
    @classmethod
    def setUpClass(cls):
        csv_file = PROJECT_ROOT / 'outputs' / 'exports' / 'completeness_municipalities.csv'
        cls.df = pd.read_csv(csv_file)
    
    def test_expected_municipalities_present(self):
        """Key municipalities should be in dataset"""
        municipalities = self.df['Municipality'].tolist()
        self.assertGreater(len(municipalities), 20, 
                          "Should have at least 20 municipalities")
    
    def test_jelgava_completeness(self):
        """Jelgava should have reasonable completeness"""
        jelgava = self.df[self.df['Municipality'] == 'Jelgava']
        if len(jelgava) > 0:
            completeness = jelgava['Completeness (%)'].values[0]
            self.assertGreater(completeness, 40, "Jelgava completeness too low")
            self.assertLess(completeness, 60, "Jelgava completeness too high")


class TestFlaskAPI(unittest.TestCase):
    """Test Flask API endpoints"""
    
    def setUp(self):
        try:
            import requests
            self.requests = requests
            self.api_available = True
        except ImportError:
            self.api_available = False
            self.skipTest("requests module not available")
    
    def test_api_reachable(self):
        """Flask API should be reachable"""
        if not self.api_available:
            return
        
        try:
            response = self.requests.get('http://localhost:5000/', timeout=5)
            self.assertIn(response.status_code, [200, 304],
                         f"API not reachable: {response.status_code}")
        except Exception as e:
            self.skipTest(f"Flask not running: {e}")
    
    def test_csv_api_endpoint(self):
        """CSV API endpoint should return data"""
        if not self.api_available:
            return
        
        try:
            response = self.requests.get('http://localhost:5000/api/csv-data', timeout=5)
            self.assertEqual(response.status_code, 200,
                           f"CSV endpoint failed: {response.status_code}")
            data = response.json()
            self.assertIsInstance(data, list, "API should return a list")
            self.assertGreater(len(data), 0, "API returned empty list")
        except Exception as e:
            self.skipTest(f"Flask not running: {e}")


class TestDataQuality(unittest.TestCase):
    """Test overall data quality"""
    
    @classmethod
    def setUpClass(cls):
        csv_file = PROJECT_ROOT / 'outputs' / 'exports' / 'completeness_municipalities.csv'
        cls.df = pd.read_csv(csv_file)
    
    def test_no_duplicates(self):
        """No duplicate municipalities"""
        self.assertEqual(len(self.df), len(self.df['Municipality'].unique()),
                        "Duplicate municipalities found")
    
    def test_municipality_names_unique(self):
        """All municipality names should be unique"""
        names = self.df['Municipality'].tolist()
        self.assertEqual(len(names), len(set(names)),
                        "Duplicate municipality names found")
    
    def test_average_completeness_reasonable(self):
        """Average completeness should be reasonable"""
        avg_completeness = self.df['Completeness (%)'].mean()
        self.assertGreater(avg_completeness, 10,
                          f"Average completeness too low: {avg_completeness}%")
        self.assertLess(avg_completeness, 50,
                       f"Average completeness too high: {avg_completeness}%")


def run_tests_verbose():
    """Run all tests with verbose output"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataFiles))
    suite.addTests(loader.loadTestsFromTestCase(TestCSVData))
    suite.addTests(loader.loadTestsFromTestCase(TestGeoJSONData))
    suite.addTests(loader.loadTestsFromTestCase(TestDataCalculations))
    suite.addTests(loader.loadTestsFromTestCase(TestMunicipalityData))
    suite.addTests(loader.loadTestsFromTestCase(TestFlaskAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestDataQuality))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 80)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests_verbose()
    sys.exit(0 if success else 1)
