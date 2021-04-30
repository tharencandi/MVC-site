<!-- Basic markdown syntax: https://www.markdownguide.org/cheat-sheet -->
<!-- Render markdown to pdf: `pandoc <filename>.md -o <filename>.pdf`-->
<!-- Tweak this to your liking-->

<!-- Some API documentation example: https://docs.github.com/en/rest/reference -->

# API Documentation

## Description

Bla bla bla

## User methods

### Summary

| Endpoint           | HTTP Method | Description          |
| ------------------ | ----------- | -------------------- |
| `/api/v1/user/xyz` | GET         | Returns random stuff |

### Details

#### `/api/v1/user/xyz`

Description here.

* Method: GET

##### Parameters
| Name | Type   | Description |
| ---- | ------ | ----------- |
| ???  | String | ???         |

##### Response
* Code: 200 OK
```json
{
"key": "value"
}
```


## Forum methods

### Summary

| Endpoint                    | HTTP Method | Description |
| --------------------------- | ----------- | ----------- |
| `/api/v1/forum/create_post` | POST        | ???         |

### Details

#### `/api/v1/forum/create_post`

Description here.

* Method: GET

##### Parameters
| Name | Type   | Description |
| ---- | ------ | ----------- |
| ???  | String | ???         |


##### Response
* Code: 200 OK
```json
{
"subject": "abc", "body": "asdf" 
}
```
