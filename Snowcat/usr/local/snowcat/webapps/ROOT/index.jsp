<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<html>
<head>
    <title>Neighborhood Weather Monitoring Station</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>
<body>
<div class="login-container">
    <h1>Welcome to the Neighborhood Weather Monitoring Station</h1>
    <form action="login.jsp" method="post" style="display: flex; flex-direction: column; gap: 10px; align-items: flex-start;">
        <div style="display: flex; justify-content: space-between; width: 100%;">
            <label for="username" style="flex: 1; text-align: left;">Username:</label>
            <input type="text" id="username" name="username" required style="flex: 2; text-align: right;">
        </div>
        <div style="display: flex; justify-content: space-between; width: 100%;">
            <label for="password" style="flex: 1; text-align: left;">Password:</label>
            <input type="password" id="password" name="password" required style="flex: 2; text-align: right;">
        </div>
        <button type="submit" style="align-self: center;">Login</button>
    </form>
</div>
<script src="snowflakes.js"></script>
</body>
</html>