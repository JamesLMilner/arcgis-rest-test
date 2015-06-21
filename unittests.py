__author__ = 'James'

# t = time_function(get_arcgis_app_token, { 'client_id' : '3tVK3X3sK4xHuhVf', 'client_secret' : '2f2e994d3aaa4da58050014912c44f42','expiration' : '1440'}, 1, "mean")
#
#
# print(get_service_type(url))
# size = get_service_size(url)
# print size
# print(get_service_views(url))
# print(get_service_name(url))

import unittest
import arcgisresttest

# Here's our "unit tests".
class helperFunctionTests(unittest.TestCase):

    def testGetBaseUrl(self):
        url = "http://services.arcgis.com/Qo2anKIAMzIEkIJB/arcgis/rest/services/TubeMap/FeatureServer/"
        self.assertEquals(arcgisresttest.get_base_url(url), "http://services.arcgis.com/")

    def testGetFullPath(self):
        url = "http://services.arcgis.com/Qo2anKIAMzIEkIJB/arcgis/rest/services/TubeMap/FeatureServer/"
        self.assertEquals(arcgisresttest.get_fullpath_url(url), "http://services.arcgis.com/Qo2anKIAMzIEkIJB/arcgis/rest/services/TubeMap/FeatureServer/")

    def testDictToStr(self):
        a_dict = {"1": "test", "2": "test2"}
        self.assertEquals(arcgisresttest.dict_to_str(a_dict), '{"1": "test", "2": "test2"}' )

    def testQueryParamsToDict(self):
        url = "http://services.arcgis.com/Qo2anKIAMzIEkIJB/arcgis/rest/services/TubeMap/FeatureServer/?f=json"
        self.assertEquals(arcgisresttest.query_params_to_dict(url), {"f":"json"})

    def testQueryParamsToDict(self):
        url = "http://services.arcgis.com/Qo2anKIAMzIEkIJB/arcgis/rest/services/TubeMap/FeatureServer/"
        self.assertIsNotNone(arcgisresttest.request_html(url))
        self.assertIsInstance(arcgisresttest.request_html(url), str)

    def testGetServiceType(self):
        url = "http://services.arcgis.com/Qo2anKIAMzIEkIJB/ArcGIS/rest/services/TubeMap/FeatureServer/1"
        self.assertEquals(arcgisresttest.get_service_type(url), "Feature Layer")

    def testGetServiceFormats(self):
        url = "http://sampleserver6.arcgisonline.com/arcgis/rest/services/CharlotteLAS/ImageServer"
        self.assertEquals(arcgisresttest.get_service_formats(url), "JSON")



def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(helperFunctionTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()