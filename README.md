rest-on-sets
============

This application allows the Users to create Sets, perform Set operations all over the standard REST interface.  Here are the end-points supported  and their behavior.


Supported Endpoints
===================
| VERB  | URI  |   Behavior|
|---|---|---|
|GET   |  /api/v1/sets |  Lists all the Sets created in the system. |
|POST   | /api/v1/sets   | Create a new Set.   |
|GET   |  /api/v1/sets/{id} | Gives back the details for the given id.  |
|DELETE   | /api/v1/sets/{id}  |  Deletes the Set for the given id. |
|POST   | /api/v1/sets/{id}/members  |  Add new member elements for the Set represented by the id. |
|DELETE   | /api/v1/sets/{id}/members  |  Remove member elements form the set represented by the id. |
|GET   |  /api/v1/sets/{id}/cardinality | Returns the cardinality for the given Set. |
|GET   |  /api/v1/sets/{l\_id}/union/{r\_id} |  Returns the union of two sets represented by l\_id and r\_id. |
|GET   |  /api/v1/sets/{l\_id}/intersection/{r\_id} | Returns the intersection of two sets represented by l\_id and r\_id.  |
|GET   |  /api/v1/sets/{l\_id}/difference/{r\_id} | Returns the difference of two sets represented by l\_id and r\_id.  |
|GET   |  /api/v1/sets/{l\_id}/sdifference/{r\_id} |  Returns the symmetric difference of two sets represented by l\_id and r\_id. |


Tutorial
--------
In this short tutorial, we will see how to interact with the APIs and get the desired results. We will use curl utility to demonstrate the same.

1. Find out how many sets does exits in our system.
	```
	curl -i 127.0.0.1:8000/api/v1/sets
	
	HTTP/1.0 200 OK
	Date: Fri, 05 Sep 2014 11:27:39 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	Cache-Control: no-cache
	
	{"meta": {"limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 0}, "objects": []}
	
	```
	As we can see, the total_count is 0 and we have empty objects list. Lets create couple of Sets next.

2. Create two sets for instance, Shapes and Pocker:
	```
	 curl -i -X POST 127.0.0.1:8000/api/v1/sets -d '{"title": "shapes", "members": ["circle", "square", "rectangle", "diamond", "heart"]}' -H "CONTENT-TYPE: application/json"
	
		HTTP/1.0 201 CREATED
		Date: Fri, 05 Sep 2014 11:28:44 GMT
		Server: WSGIServer/0.1 Python/2.7.3
		Vary: Accept
		X-Frame-Options: SAMEORIGIN
		Content-Type: text/html; charset=utf-8
		Location: http://127.0.0.1:8000/api/v1/sets/6f41b97bd5be453698b8309741cda6a4
	```
	
	```
	curl -i -X POST 127.0.0.1:8000/api/v1/sets -d '{"title": "shapes", "members": ["diamond", "heart", "turn", "spade"]}' -H "CONTENT-TYPE: application/json"
	
	HTTP/1.0 201 CREATED
	Date: Fri, 05 Sep 2014 11:29:08 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: text/html; charset=utf-8
	Location: http://127.0.0.1:8000/api/v1/sets/95c2fcb8a7bd4812a51f554efb908535
	```
	Two important pieces of information from the output are - Status code: 201 Created and Location header: this gives us the URI for newly created object.
	
	And now, check the collection of sets in the system:
	```
	curl -i 127.0.0.1:8000/api/v1/sets
	
	HTTP/1.0 200 OK
	Date: Fri, 05 Sep 2014 11:30:51 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	Cache-Control: no-cache
	
	{"meta": {"limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 2}, "objects": [{"id": "95c2fcb8a7bd4812a51f554efb908535", "members": ["heart", "diamond", "spade", "turn"], "resource_uri": "/api/v1/sets/95c2fcb8a7bd4812a51f554efb908535", "title": "shapes"}, {"id": "6f41b97bd5be453698b8309741cda6a4", "members": ["heart", "circle", "square", "rectangle", "diamond"], "resource_uri": "/api/v1/sets/6f41b97bd5be453698b8309741cda6a4", "title": "shapes"}]}
	```
	As expected, total_count is 2 and we have both the sets in the objects list.

3. We can fetch the details for individual Set by passing the id.
	```
		curl -i 127.0.0.1:8000/api/v1/sets/6f41b97bd5be453698b8309741cda6a4
	
	HTTP/1.0 200 OK
	Date: Fri, 05 Sep 2014 11:32:05 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	Cache-Control: no-cache
	
	{"id": "6f41b97bd5be453698b8309741cda6a4", "members": ["heart", "circle", "square", "rectangle", "diamond"], "resource_uri": "/api/v1/sets/6f41b97bd5be453698b8309741cda6a4", "title": "shapes"}
	```
	
	```
	curl -i 127.0.0.1:8000/api/v1/sets/95c2fcb8a7bd4812a51f554efb908535
	
	HTTP/1.0 200 OK
	Date: Fri, 05 Sep 2014 11:32:44 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	Cache-Control: no-cache
	
	{"id": "95c2fcb8a7bd4812a51f554efb908535", "members": ["heart", "diamond", "spade", "turn"], "resource_uri": "/api/v1/sets/95c2fcb8a7bd4812a51f554efb908535", "title": "shapes"}
	```
4. Try checking the cardinality for both the sets.
	```
	curl -i 127.0.0.1:8000/api/v1/sets/6f41b97bd5be453698b8309741cda6a4/cardinality
	
	HTTP/1.0 200 OK
	Date: Fri, 05 Sep 2014 11:33:27 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	Cache-Control: no-cache
	
	{"cardinality": 5}
	```
	```
	curl -i 127.0.0.1:8000/api/v1/sets/95c2fcb8a7bd4812a51f554efb908535/cardinality
	
	HTTP/1.0 200 OK
	Date: Fri, 05 Sep 2014 11:35:12 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	Cache-Control: no-cache
	
	{"cardinality": 4}
	```
5. Try adding new members in _shapes_ set.
	```
	curl -i -X POST 127.0.0.1:8000/api/v1/sets/6f41b97bd5be453698b8309741cda6a4/members -d '{"members": ["triangle", "diamond"]}' -H "CONTENT-TYPE: application/json"
	
	HTTP/1.0 202 ACCEPTED
	Date: Fri, 05 Sep 2014 11:36:09 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	
	{"id": "6f41b97bd5be453698b8309741cda6a4", "members": ["heart", "square", "triangle", "diamond", "circle", "rectangle"], "resource_uri": "/api/v1/sets/6f41b97bd5be453698b8309741cda6a4", "title": "shapes"}
	```
	Now, if we try getting the details for the Shapes set, we should get the new members we added.
	```
	curl -i 127.0.0.1:8000/api/v1/sets/6f41b97bd5be453698b8309741cda6a4
	
	HTTP/1.0 200 OK
	Date: Fri, 05 Sep 2014 11:37:02 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	Cache-Control: no-cache
	
	{"id": "6f41b97bd5be453698b8309741cda6a4", "members": ["heart", "square", "triangle", "diamond", "circle", "rectangle"], "resource_uri": "/api/v1/sets/6f41b97bd5be453698b8309741cda6a4", "title": "shapes"}
	```
	Notice that there isn't duplicate entry for diamond. Lets now check the cardinality for the Shapes:
	
	```
	curl -i 127.0.0.1:8000/api/v1/sets/6f41b97bd5be453698b8309741cda6a4/cardinality
	
	HTTP/1.0 200 OK
	Date: Fri, 05 Sep 2014 11:38:18 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	Cache-Control: no-cache
	
	{"cardinality": 6}
	```
6. Lets go back to where we were, and try deleting the new members we added.
	```
	curl -i -X DELETE 127.0.0.1:8000/api/v1/sets/6f41b97bd5be453698b8309741cda6a4/members -d '{"members": ["triangle"]}' -H "CONTENT-TYPE: application/json"
	
	HTTP/1.0 202 ACCEPTED
	Date: Fri, 05 Sep 2014 11:39:18 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	
	{"id": "6f41b97bd5be453698b8309741cda6a4", "members": ["heart", "square", "diamond", "circle", "rectangle"], "resource_uri": "/api/v1/sets/6f41b97bd5be453698b8309741cda6a4", "title": "shapes"}
	```
	And of course, we can check the details and cardinality to make sure they are consistent.
	
	```
	curl -i 127.0.0.1:8000/api/v1/sets/6f41b97bd5be453698b8309741cda6a4/cardinality
	
	HTTP/1.0 200 OK
	Date: Fri, 05 Sep 2014 11:39:54 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	Cache-Control: no-cache
	
	{"cardinality": 5}
	```
	
	```
	curl -i 127.0.0.1:8000/api/v1/sets/6f41b97bd5be453698b8309741cda6a4
	
	HTTP/1.0 200 OK
	Date: Fri, 05 Sep 2014 11:40:16 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	Cache-Control: no-cache
	
	{"id": "6f41b97bd5be453698b8309741cda6a4", "members": ["heart", "square", "diamond", "circle", "rectangle"], "resource_uri": "/api/v1/sets/6f41b97bd5be453698b8309741cda6a4", "title": "shapes"}
	```

7. Try finding the union of shapes and pocker.
	```
	curl -i 127.0.0.1:8000/api/v1/sets/6f41b97bd5be453698b8309741cda6a4/union/95c2fcb8a7bd4812a51f554efb908535
	
	HTTP/1.0 200 OK
	Date: Fri, 05 Sep 2014 11:42:29 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	Cache-Control: no-cache
	
	{"members": ["heart", "diamond", "square", "spade", "turn", "circle", "rectangle"]}
	```
8. Try finding the intersection of shapes and pocker.
	```
	curl -i 127.0.0.1:8000/api/v1/sets/6f41b97bd5be453698b8309741cda6a4/intersection/95c2fcb8a7bd4812a51f554efb908535
	
	HTTP/1.0 200 OK
	Date: Fri, 05 Sep 2014 11:42:52 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	Cache-Control: no-cache
	
	{"members": ["heart", "diamond"]}
	```
9. Lets now check the difference of the two.
	```
	curl -i 127.0.0.1:8000/api/v1/sets/6f41b97bd5be453698b8309741cda6a4/difference/95c2fcb8a7bd4812a51f554efb908535
	
	HTTP/1.0 200 OK
	Date: Fri, 05 Sep 2014 11:43:13 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	Cache-Control: no-cache
	
	{"members": ["square", "circle", "rectangle"]}
	```
10. And, finding the symmetric difference as well.
	```
	curl -i 127.0.0.1:8000/api/v1/sets/6f41b97bd5be453698b8309741cda6a4/sdifference/95c2fcb8a7bd4812a51f554efb908535
	
	HTTP/1.0 200 OK
	Date: Fri, 05 Sep 2014 11:43:32 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	Cache-Control: no-cache
	
	{"members": ["square", "spade", "turn", "circle", "rectangle"]}
	```
11. Hmm, so we did perform most of the operations, lets now try deleting both the Sets:
	```
	curl -i -X DELETE 127.0.0.1:8000/api/v1/sets/6f41b97bd5be453698b8309741cda6a4
	
	HTTP/1.0 204 NO CONTENT
	Date: Fri, 05 Sep 2014 11:43:56 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: text/html; charset=utf-8
	Content-Length: 0
	```
	
	```
	curl -i -X DELETE 127.0.0.1:8000/api/v1/sets/95c2fcb8a7bd4812a51f554efb908535
	
	HTTP/1.0 204 NO CONTENT
	Date: Fri, 05 Sep 2014 11:44:16 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: text/html; charset=utf-8
	Content-Length: 0
	```
	
	And now, if we check the set listing API, we should not get any Set in the results
	
	```
	curl -i 127.0.0.1:8000/api/v1/sets
	
	HTTP/1.0 200 OK
	Date: Fri, 05 Sep 2014 11:44:37 GMT
	Server: WSGIServer/0.1 Python/2.7.3
	Vary: Accept
	X-Frame-Options: SAMEORIGIN
	Content-Type: application/json
	Cache-Control: no-cache
	
	{"meta": {"limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 0}, "objects": []}
	```
	
	Notice, the total_count is 0 and the there aren't any objects in the system.



> NOTE:
> Everything in this application is transient and stored in memory. All the sets we create are therefore lost when we restart the application.
