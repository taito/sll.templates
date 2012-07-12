# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from hexagonit.testing.browser import Browser
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.testing import layered
from sll.templates.tests.base import FUNCTIONAL_TESTING
from zope.interface import alsoProvides
from zope.testing import renormalizing

import doctest
import manuel.codeblock
import manuel.doctest
import manuel.testing
import re
import transaction
import unittest2 as unittest

FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS | doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE

CHECKER = renormalizing.RENormalizing([
    # Normalize the generated UUID values to always compare equal.
    (re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'), '<UUID>'),
])


def setUp(self):
    layer = self.globs['layer']
    # Update global variables within the tests.
    self.globs.update({
        'portal': layer['portal'],
        'portal_url': layer['portal'].absolute_url(),
        'browser': Browser(layer['app']),
        'TEST_USER_ID': TEST_USER_ID,
        'TEST_USER_NAME': TEST_USER_NAME,
        'TEST_USER_PASSWORD': TEST_USER_PASSWORD,
    })

    portal = self.globs['portal']
    browser = self.globs['browser']
    portal_url = self.globs['portal_url']
    browser.setBaseUrl(portal_url)

    browser.handleErrors = True
    portal.error_log._ignored_exceptions = ()

    setRoles(portal, TEST_USER_ID, ['Site Administrator'])

    user2 = 'test_user_2_'
    regtool = getToolByName(portal, 'portal_registration')
    regtool.addMember(user2, user2)
    setRoles(portal, user2, ['Contributor'])
    self.globs['user2'] = user2

    folder1 = portal[portal.invokeFactory('Folder', 'folder1', title="Földer1")]
    # INavigationRoot for folder1.
    alsoProvides(folder1, INavigationRoot)
    folder1.reindexObject()
    folder2 = portal[portal.invokeFactory('Folder', 'folder2', title="Földer2")]
    # INavigationRoot for folder2.
    alsoProvides(folder1, INavigationRoot)
    folder2.reindexObject()
    doc1 = folder1[folder1.invokeFactory(
        'Document', 'doc1', title="Döcument1", description="Description of Döcument1")]
    doc1.reindexObject()



    transaction.commit()


def DocFileSuite(testfile, flags=FLAGS, setUp=setUp, layer=FUNCTIONAL_TESTING):
    """Returns a test suite configured with a test layer.

    :param testfile: Path to a doctest file.
    :type testfile: str

    :param flags: Doctest test flags.
    :type flags: int

    :param setUp: Test set up function.
    :type setUp: callable

    :param layer: Test layer
    :type layer: object

    :rtype: `manuel.testing.TestSuite`
    """
    m = manuel.doctest.Manuel(optionflags=flags, checker=CHECKER)
    m += manuel.codeblock.Manuel()

    return layered(
        manuel.testing.TestSuite(m, testfile, setUp=setUp, globs=dict(layer=layer)),
        layer=layer)


def test_suite():
    return unittest.TestSuite([
        DocFileSuite('functional/portal_sll_view.txt'),
        ])
