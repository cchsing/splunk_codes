# Entuity Addon for Splunk

1. to test the HEC

```
curl "https://10.111.32.159:8088/services/collector/raw" -H 'Authorization: Splunk 3dea80b9-092a-4d5a-bb38-9172b558a85e' -d '{"event":"Hello, world!"}' -k
```

- IP: 10.111.32.159
- Port: 8088
- Endpoint: /services/collector/raw
- Token: 3dea80b9-092a-4d5a-bb38-9172b558a85e
