-- Total number of patients
SELECT COUNT(*) AS total_patients
FROM dbo.hospital_readmissions;

-- Readmission Rate
SELECT
    readmitted,
    COUNT(*) AS patient_count,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS DECIMAL(5,2)) AS percentage
FROM dbo.hospital_readmissions
GROUP BY readmitted;
-- Length of Stay Comparison
SELECT
    readmitted,
    AVG(length_of_stay) AS avg_length_of_stay
FROM dbo.hospital_readmissions
GROUP BY readmitted;

-- Readmission by Discharge Destination
SELECT
    discharge_destination,
    COUNT(*) AS total_patients,
    SUM(CASE WHEN readmitted = 1 THEN 1 ELSE 0 END) AS readmitted_patients,
    CAST(
        SUM(CASE WHEN readmitted = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
        AS DECIMAL(5,2)
    ) AS readmission_rate
FROM dbo.hospital_readmissions
GROUP BY discharge_destination
ORDER BY readmission_rate DESC;

-- Clinical Conditions vs Readmission
SELECT
    diabetes,
    CAST(AVG(CAST(readmitted AS FLOAT)) * 100 AS DECIMAL(5,2)) AS readmission_rate
FROM dbo.hospital_readmissions
GROUP BY diabetes;
SELECT
    hypertension,
    CAST(AVG(CAST(readmitted AS FLOAT)) * 100 AS DECIMAL(5,2)) AS readmission_rate
FROM dbo.hospital_readmissions
GROUP BY hypertension;

-- Medication Burden
SELECT
    hypertension,
    CAST(AVG(CAST(readmitted AS FLOAT)) * 100 AS DECIMAL(5,2)) AS readmission_rate
FROM dbo.hospital_readmissions
GROUP BY hypertension;
