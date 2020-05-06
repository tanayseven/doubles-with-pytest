from typing import List


class S3DummyResource:
    def __init__(self, *args, **kwargs):
        pass

    def Bucket(self, *args, **kwargs):
        class DummyBucket:
            def put_object(self, *args, **kwargs):
                class Object:
                    def __init__(self):
                        self.key = None

                return Object()

        return DummyBucket()


class S3MockExpectation:
    def __init__(self):
        self._put_object_called = False

    @property
    def is_put_object_called(self) -> bool:
        return self._put_object_called

    def _set_put_object_called(self):
        self._put_object_called = True

    def __call__(self, *args, **kwargs):
        put_object_called = self._set_put_object_called

        class S3MockResource:
            def __init__(self, *args, **kwargs):
                pass

            def Bucket(self, *args, **kwargs):
                class DummyBucket:
                    def __init__(self, *args, **kwargs):
                        pass

                    def put_object(self, *args, **kwargs):
                        put_object_called()

                        class Object:
                            def __init__(self):
                                self.key = None

                        return Object()

                return DummyBucket()

        return S3MockResource


class S3SpyExpectation:

    def __init__(self):
        self._put_object_call_count = 0

    def put_object_is_called(self, times=0) -> bool:
        return self._put_object_call_count == times

    def _increment_put_object_called(self):
        self._put_object_call_count += 1

    def __call__(self, *args, **kwargs):
        put_object_called = self._increment_put_object_called

        class S3SpyResource:
            def __init__(self, *args, **kwargs):
                pass

            def Bucket(self, *args, **kwargs):
                class DummyBucket:
                    def __init__(self, *args, **kwargs):
                        pass

                    def put_object(self, *args, **kwargs):
                        put_object_called()

                        class Object:
                            def __init__(self):
                                self.key = None

                        return Object()

                return DummyBucket()

        return S3SpyResource


class S3StubbedSetup:
    def __init__(self):
        self._put_object_return_counter = 0
        self._put_object_return_list: List[object] = []

    def put_object_return_list_current_count(self):
        if self._put_object_return_counter >= len(self._put_object_return_list):
            raise IndexError('Exceeded the total number of stubs provided')
        return self._put_object_return_counter

    def _increment_put_object_return_counter(self):
        self._put_object_return_counter += 1

    def allow_put_object_to_return(self, objects: List[object]):
        self._put_object_return_list = objects

    def __call__(self, *args, **kwargs):
        put_object_return_list = self._put_object_return_list
        put_object_return_list_current_count = self.put_object_return_list_current_count
        increment_put_object_return_counter = self._increment_put_object_return_counter

        class S3StubbedResource:
            def __init__(self, *args, **kwargs):
                pass

            def Bucket(self, *args, **kwargs):
                class DummyBucket:
                    def put_object(self, *args, **kwargs):
                        class Object:
                            def __init__(self):
                                self.key = None

                        count = put_object_return_list_current_count()
                        increment_put_object_return_counter()
                        return put_object_return_list[count]

                return DummyBucket()

        return S3StubbedResource


class StubObject:
    def __init__(self, key):
        self.key = key