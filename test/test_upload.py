import json
from io import BytesIO

import boto3

from test.doubles import S3DummyResource, S3MockExpectation, S3SpyExpectation, S3StubbedSetup, StubObject
from test.fake_boto import fake_boto_resource


def test_upload_succeeds_with_dummy(client, monkeypatch):
    # given
    monkeypatch.setattr(boto3, 'resource', S3DummyResource)
    request_data = {
        'file_1': (BytesIO(b'my file contents'), 'test_file.txt', 'text/plain'),
    }

    # when
    response = client.post(
        '/upload',
        content_type='multipart/form-data',
        data=request_data,
    )

    # then
    assert response.status_code == 200


def test_upload_fails_with_dummy(client, monkeypatch):
    # given
    monkeypatch.setattr(boto3, 'resource', S3DummyResource)
    request_data = {}

    # when
    response = client.post(
        '/upload',
        content_type='multipart/form-data',
        data=request_data,
    )

    # then
    assert response.status_code == 400


def test_upload_succeeds_with_mock(client, monkeypatch):
    # given
    s3_mock_resource_expectation = S3MockExpectation()
    monkeypatch.setattr(boto3, 'resource', s3_mock_resource_expectation)
    request_data = {
        'file_1': (BytesIO(b'my file contents'), 'test_file.txt', 'text/plain'),
    }

    # when
    response = client.post(
        '/upload',
        content_type='multipart/form-data',
        data=request_data,
    )

    # then
    assert response.status_code == 200
    assert s3_mock_resource_expectation.is_put_object_called


def test_upload_fails_with_mock(client, monkeypatch):
    # given
    s3_mock_resource_expectation = S3MockExpectation()
    monkeypatch.setattr(boto3, 'resource', s3_mock_resource_expectation)
    request_data = {}

    # when
    response = client.post(
        '/upload',
        content_type='multipart/form-data',
        data=request_data,
    )

    # then
    assert response.status_code == 400
    assert not s3_mock_resource_expectation.is_put_object_called


def test_upload_succeeds_with_spy(client, monkeypatch):
    # given
    s3_spy_resource_expectation = S3SpyExpectation()
    monkeypatch.setattr(boto3, 'resource', s3_spy_resource_expectation)
    request_data = {
        'file_1': (BytesIO(b'my file contents'), 'test_file.txt', 'text/plain'),
    }

    # when
    response = client.post(
        '/upload',
        content_type='multipart/form-data',
        data=request_data,
    )

    # then
    assert response.status_code == 200
    assert s3_spy_resource_expectation.put_object_is_called(times=1)


def test_upload_fails_with_spy(client, monkeypatch):
    # given
    s3_spy_resource_expectation = S3SpyExpectation()
    monkeypatch.setattr(boto3, 'resource', s3_spy_resource_expectation)
    request_data = {}

    # when
    response = client.post(
        '/upload',
        content_type='multipart/form-data',
        data=request_data,
    )

    # then
    assert response.status_code == 400
    assert s3_spy_resource_expectation.put_object_is_called(times=0)


def test_upload_succeeds_with_stub(client, monkeypatch):
    # given
    stubbed_object = StubObject(key='test_file.txt')
    stubbed_setup = S3StubbedSetup()
    stubbed_setup.allow_put_object_to_return([stubbed_object])
    monkeypatch.setattr(boto3, 'resource', stubbed_setup)
    request_data = {
        'file_1': (BytesIO(b'my file contents'), 'test_file.txt', 'text/plain'),
    }

    # when
    response = client.post(
        '/upload',
        content_type='multipart/form-data',
        data=request_data,
    )

    # then
    response_content = json.loads(response.data)
    assert response.status_code == 200
    assert response_content['objects_uploaded'][0] == 'test_file.txt'


def test_upload_succeeds_with_fake(client, monkeypatch):
    # given
    monkeypatch.setattr(boto3, 'resource', fake_boto_resource)
    request_data = {
        'file_1': (BytesIO(b'my file contents'), 'test_file.txt', 'text/plain'),
    }

    # when
    response = client.post(
        '/upload',
        content_type='multipart/form-data',
        data=request_data,
    )

    # then
    response_content = json.loads(response.data)
    assert response.status_code == 200
    assert response_content['objects_uploaded'][0] == 'test_file.txt'
