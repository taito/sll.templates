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
import unittest

FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS | doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE

CHECKER = renormalizing.RENormalizing([
    # Normalize the generated UUID values to always compare equal.
    (re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'), '<UUID>'),
])


def setUp(self):
    layer = self.globs['layer']
    browser = Browser(layer['app'])
    portal = layer['portal']
    # Update global variables within the tests.
    self.globs.update({
        'TEST_USER_NAME': TEST_USER_NAME,
        'TEST_USER_PASSWORD': TEST_USER_PASSWORD,
        'browser': browser,
        'portal': portal,
    })

    browser.setBaseUrl(portal.absolute_url())
    browser.handleErrors = True
    portal.error_log._ignored_exceptions = ()
    setRoles(portal, TEST_USER_ID, ['Site Administrator'])
    # setRoles(portal, TEST_USER_ID, ['Manager'])

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
    doc1.setEffectiveDate(doc1.modified())
    doc1.reindexObject()
    desc = 'Ä' * 201
    doc2 = folder2[folder2.invokeFactory(
        'Document', 'doc2', title="Döcument2", description=desc)]
    doc2.setEffectiveDate(doc2.modified())
    doc2.reindexObject()

    ajankohtaista = portal[portal.invokeFactory('Folder', 'ajankohtaista', title="Ajankohtaista")]
    ajankohtaista.setEffectiveDate(ajankohtaista.modified())
    ajankohtaista.reindexObject()

    news1 = ajankohtaista[ajankohtaista.invokeFactory(
        'News Item', 'news1', title="News1", description="Descriptiön of News1")]
    # news1.setEffectiveDate(news1.modified())
    news1.reindexObject()

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
    return unittest.TestSuite([DocFileSuite('functional/portal-sll-view.txt')])
