# airdb-TB

## Development

### Build and Run

Build the Docker image:

```bash
docker build -f Dockerfile.dev -t tb-dev . --no-cache
```

Run the container:

> **Warning**: This command mounts your local ./app directory into the container.
**Any changes made inside the container—including edits, moves, or deletions—will affect your local files as well.**
There is no safety buffer: deleting a file in the container deletes it on your machine.

```bash
docker run -p 8003:8000 \
  --name tb-container \
  -v $(pwd)/app:/code/app \
  --rm tb-dev
```

The backend will now be available at: http://127.0.0.1:8003

To enter the running container for debugging:

```bash
docker exec -it tb-container /bin/bash
```

### API Usage

####  Endpoint: POST /predict

**RequestParameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `sex` | integer | Patient sex: `0` = Female, `1` = Male |
| `age` | integer | Patient's age in years |
| `address` | string | Site address |
| `id` | string | Medical record ID |
| `date` | string | Air pollution baseline date |
| `dis_list` | array | Array of 14 binary values (0 or 1) indicating presence of diseases |
| `air_data` | object | Air quality measurements (so2, co, o3, pm10, pm2.5, no2, nox, no) |

**Disease List (`dis_list`)**

An array of 14 binary values (0 = absent, 1 = present) in the following order:
1. HBV
2. HCV
3. Cancer
4. Dementia
5. Hyperlipidemia
6. DiabetesMellitus
7. MyocardialInfraction
8. ChronicKidneyDisease
9. CerebrovascularDiease
10. CongestiveHeartFailure
11. PeripheralVascularDisease
12. Pneumonia
13. ObstructiveLungDisease
14. AcuteRenalFailure

**Example request:**

```bash
curl -X POST "http://127.0.0.1:8003/predict" \
  -H "Content-Type: application/json" \
  -d '{
        "sex": 0, 
        "age": 18, 
        "address": "高雄市鼓山區蓮海路70號", 
        "id": "1", 
        "date": "2025-09-17", 
        "dis_list": [
            1,
            1,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ], 
        "air_data": {
            "so2": 0.48,
            "co": 0.23,
            "o3": 31.16,
            "pm10": 26.17,
            "pm2.5": 12.07,
            "no2": 8.67,
            "nox": 9.68,
            "no": 0.97
        }
      }'
```

**Example response:**

```bash
3.123
```