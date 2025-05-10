using System.Collections.Generic;
using UnityEngine;
using CesiumForUnity;

public class DisasterPointSpawner : MonoBehaviour
{
    public TextAsset csvFile;
    public GameObject pointPrefab;
    public CesiumGeoreference georeference;

    private List<GameObject> spawnedPoints = new List<GameObject>();

    void Start()
    {
        if (!ValidateReferences()) return;
        ParseCSV();
    }

    bool ValidateReferences()
    {
        if (csvFile == null) Debug.LogError("CSV file not assigned!");
        if (pointPrefab == null) Debug.LogError("Point prefab not assigned!");
        if (georeference == null) Debug.LogError("CesiumGeoreference not assigned!");
        return csvFile != null && pointPrefab != null && georeference != null;
    }

    void ParseCSV()
    {
        string[] lines = csvFile.text.Split('\n');
        for (int i = 1; i < lines.Length; i++)
        {
            if (string.IsNullOrWhiteSpace(lines[i])) continue;
            ProcessCSVLine(lines[i], i);
        }
    }

    void ProcessCSVLine(string line, int lineNumber)
    {
        string[] values = line.Split(',');
        if (values.Length < 4)
        {
            Debug.LogWarning($"Line {lineNumber}: Insufficient data");
            return;
        }

        string id = values[0].Trim();
        if (!double.TryParse(values[1].Trim(), out double latitude) ||
            !double.TryParse(values[2].Trim(), out double longitude) ||
            !double.TryParse(values[3].Trim(), out double height))
        {
            Debug.LogWarning($"Line {lineNumber}: Invalid coordinates");
            return;
        }

        CreateDisasterPoint(id, longitude, latitude, height);
    }

    void CreateDisasterPoint(string id, double longitude, double latitude, double height)
    {
        GameObject point = Instantiate(pointPrefab, georeference.transform);
        point.name = $"Disaster_{id}";
        point.transform.localScale = Vector3.one * 100f;

        var anchor = point.GetComponent<CesiumGlobeAnchor>();
        if (anchor == null)
        {
            anchor = point.AddComponent<CesiumGlobeAnchor>();
        }

        // Correct way to set coordinates in current Cesium for Unity versions
        anchor.longitude = longitude;
        anchor.latitude = latitude;
        anchor.height = height;

        spawnedPoints.Add(point);
    }

    void OnDestroy()
    {
        foreach (var point in spawnedPoints)
        {
            if (point != null) Destroy(point);
        }
    }
}