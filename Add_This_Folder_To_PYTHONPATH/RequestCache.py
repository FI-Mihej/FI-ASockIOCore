__author__ = 'ButenkoMS <gtalk@butenkoms.space>'

import time
import json


class RequestCache:
    # TODO: add GC which will clean lists every X seconds (really - every Y hours)

    def __init__(self, itemsQntLimit, timeLimitInSeconds=None, clock_function=None):
        # timeLimitInSeconds:
        # - number - limit in seconds (remember that the accuracy of the server clock is
        #   approximately 1 second);
        # - 0 (zero) - cache is not used (try_to_get_data_for_request() will return 'None'
        #   on every request);
        # - None - cache is trying to be permanent (time limit is not used at all)
        super().__init__()
        self._clock_function = clock_function or time.time
        self._itemsQntLimit = itemsQntLimit
        self._timeLimitInSeconds = timeLimitInSeconds
        self._requestsAndData = {}   # key - request; data - (data, Server Time of last change). Server Time of last
            #  change must be less or equal to self._itemsQntLimit
        self._requestsHistory = []   # [request0, request1, ..., requestN]
        self.isWasChanged = False

    def put_new_request(self, request, data):
        self._move_request_to_the_end_of_history(request)
        if request in self._requestsAndData:
            dataAndTime = self._requestsAndData[request]
            is_was_changed = False
            if isinstance(data, type(dataAndTime[0])):
                if data != dataAndTime[0]:
                    is_was_changed = True
            else:
                is_was_changed = True

            if is_was_changed:
                self._requestsAndData[request] = (data, self._clock_function())
                self.isWasChanged = True
        else:
            if len(self._requestsAndData) >= self._itemsQntLimit:
                forDeleting = self._requestsHistory[0]
                if forDeleting in self._requestsAndData:
                    del self._requestsAndData[forDeleting]
                del self._requestsHistory[0]
            self._requestsAndData[request] = (data, self._clock_function())
            self.isWasChanged = True

    def put_new_request_or_renew_it(self, request, data):
        self._move_request_to_the_end_of_history(request)
        if request in self._requestsAndData:
            dataAndTime = self._requestsAndData[request]
            self._requestsAndData[request] = (data, self._clock_function())
            self.isWasChanged = True
        else:
            if len(self._requestsAndData) >= self._itemsQntLimit:
                forDeleting = self._requestsHistory[0]
                if forDeleting in self._requestsAndData:
                    del self._requestsAndData[forDeleting]
                del self._requestsHistory[0]
            self._requestsAndData[request] = (data, self._clock_function())
            self.isWasChanged = True

    def try_to_get_raw_data_for_request(self, request):
        if request in self._requestsAndData:
            dataAndTime = self._requestsAndData[request]
            return dataAndTime[0]
        else:
            return None

    def try_to_get_raw_data_with_time_for_request(self, request):
        if request in self._requestsAndData:
            dataAndTime = self._requestsAndData[request]
            return dataAndTime
        else:
            return None

    def try_to_get_data_for_request(self, request):
        if request in self._requestsAndData:
            dataAndTime = self._requestsAndData[request]
            lastChangingTime = dataAndTime[1]
            tLimit = self._timeLimitInSeconds
            if (tLimit is not None) and ((self._clock_function() - lastChangingTime) >= tLimit):
                del self._requestsAndData[request]
                if request in self._requestsHistory:
                    self._requestsHistory.remove(request)
                return None
            else:
                self._move_request_to_the_end_of_history(request)
                return dataAndTime[0]
        else:
            return None

    def try_to_get_data_for_request_and_renew_it(self, request):
        if request in self._requestsAndData:
            dataAndTime = self._requestsAndData[request]
            lastChangingTime = dataAndTime[1]
            tLimit = self._timeLimitInSeconds
            if (tLimit is not None) and ((self._clock_function() - lastChangingTime) >= tLimit):
                del self._requestsAndData[request]
                if request in self._requestsHistory:
                    self._requestsHistory.remove(request)
                return None
            else:
                self._move_request_to_the_end_of_history(request)
                self._requestsAndData[request] = (dataAndTime[0], self._clock_function())
                self.isWasChanged = True
                return dataAndTime[0]
        else:
            return None

    def try_to_remove_request(self, request):
        if request in self._requestsAndData:
            del self._requestsAndData[request]
        if request in self._requestsHistory:
            self._requestsHistory.remove(request)

    def _move_request_to_the_end_of_history(self, request):
        if request in self._requestsAndData:
            if request in self._requestsHistory:
                self._requestsHistory.remove(request)
        self._requestsHistory.append(request)

    def update(self, anotherRequestCache):
        if type(anotherRequestCache) == RequestCache:
            self._itemsQntLimit += anotherRequestCache._itemsQntLimit
            self._requestsAndData.update(anotherRequestCache._requestsAndData)
            self.isWasChanged = True
            # Do not do this:
            # self._requestsHistory += anotherRequestCache._requestsHistory

    def clear(self):
        self._requestsAndData.clear()
        # self._requestsHistory.clear()  # Python 3.3+ only so can't be used under PyPy yet.
        del self._requestsHistory[:]
        self.isWasChanged = True

    def get_state(self):
        reqAndDat = []
        for item in self._requestsAndData.items():
            reqAndDat.append(item)
        data = (self._itemsQntLimit
                , self._timeLimitInSeconds
                , reqAndDat
                , self._requestsHistory)
        return json.dumps(data)

    def set_state(self, state):
        data = json.loads(state)
        self._itemsQntLimit = data[0]
        self._timeLimitInSeconds = data[1]
        for item in data[2]:
            self._requestsAndData[item[0]] = item[1]
        self._requestsHistory = data[3]
        self.isWasChanged = True
