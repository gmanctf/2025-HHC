<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.io.*" %>
<%@ page import="org.apache.commons.collections.map.*" %>
<html>
<head>
    <title>Neighborhood Weather Monitoring Station</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>
<body>
<div class="dashboard-container">
    <h1>Neighborhood Weather Monitoring Station</h1>
    <p>Providing real-time Neighborhood weather monitoring since 2022.</p>
    <%
        if (session == null || session.getAttribute("username") == null) {
            // No valid session, redirect to login page
            response.sendRedirect("/");
            return;
        }
        String username = (String) session.getAttribute("username");
        String firstname = (String) session.getAttribute("firstname");
        String lastname = (String) session.getAttribute("lastname");

        out.println("<h2>Welcome, " + firstname + " " + lastname + "</h2>");

        try {
            String key = "4b2f3c2d-1f88-4a09-8bd4-d3e5e52e19a6";
            Process tempProc = Runtime.getRuntime().exec("/usr/local/weather/temperature " + key);
            Process humProc = Runtime.getRuntime().exec("/usr/local/weather/humidity " + key);
            Process presProc = Runtime.getRuntime().exec("/usr/local/weather/pressure " + key);

            BufferedReader tempReader = new BufferedReader(new InputStreamReader(tempProc.getInputStream()));
            BufferedReader humReader = new BufferedReader(new InputStreamReader(humProc.getInputStream()));
            BufferedReader presReader = new BufferedReader(new InputStreamReader(presProc.getInputStream()));

            String tempLine = tempReader.readLine();
            String humLine = humReader.readLine();
            String presLine = presReader.readLine();
        
            if (tempLine == null || humLine == null || presLine == null) {
                out.println("<p>Error: Unable to retrieve weather data. Please try again later.</p>");
                return;
            }
        
            float temperature = Float.parseFloat(tempLine);
            float humidity = Float.parseFloat(humLine);
            int pressure = Integer.parseInt(presLine); // Parse pressure as integer

            // Define min and max values using Apache Commons Collections MultiValueMap
            MultiValueMap ranges = new MultiValueMap();

            ranges.put("temperature", 70.0f);
            ranges.put("temperature", -50.0f);

            ranges.put("humidity", 100.0f);
            ranges.put("humidity", 0.0f);

            ranges.put("pressure", 950);
            ranges.put("pressure", 1050);

            // Retrieve min and max values for normalization
            float tempMin = (float) ranges.getCollection("temperature").toArray()[0];
            float tempMax = (float) ranges.getCollection("temperature").toArray()[1];

            float humMin = (float) ranges.getCollection("humidity").toArray()[0];
            float humMax = (float) ranges.getCollection("humidity").toArray()[1];

            int presMin = (int) ranges.getCollection("pressure").toArray()[0];
            int presMax = (int) ranges.getCollection("pressure").toArray()[1];

            // Normalize values using the ranges
            float normalizedTemperature = (temperature - tempMin) / (float) (tempMax - tempMin);
            float normalizedHumidity = (humidity - humMin) / (humMax - humMin);
            float normalizedPressure = (pressure - presMin) / (float) (presMax - presMin);

            // Adjust weights based on normalized values for Kansas December weather
            float tempScore = temperature < 2.0f ? 1.0f : (temperature < 6.0f ? 0.5f : 0.0f);
            float humScore = humidity > 70.0f ? 1.0f : (humidity > 50.0f ? 0.5f : 0.0f);
            float presScore = pressure < 1015 ? 1.0f : (pressure < 1025 ? 0.5f : 0.0f);
            float likelihood = tempScore * 50 + humScore * 30 + presScore * 20;
            String likelihoodLevel = likelihood > 75 ? "High" : (likelihood > 50 ? "Medium" : "Low");

            out.println("<p>Likelihood of snow: <strong>" + likelihoodLevel + "</strong></p>");
            out.println("<p>Temperature: " + temperature + " °C</p>"); // Explicitly cast to integer
            out.println("<p>Humidity: " + humidity + " %</p>");
            out.println("<p>Pressure: " + (int) pressure + " hPa</p>"); // Explicitly cast to integer
        } catch (Exception e) {
            e.printStackTrace();
            out.println("<p>Error: Unable to retrieve weather data. Please try again later.</p>");
        }
    %>
</div>
<script src="snowflakes.js"></script>
</body>
</html>