<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*, java.io.*" %>
<%
    String username = request.getParameter("username");
    String password = request.getParameter("password");
    boolean authenticated = false;

    // Explicitly load the SQLite JDBC driver
    Class.forName("org.sqlite.JDBC");

    // Get the absolute path to the database file
    String dbPath = getServletContext().getRealPath("/WEB-INF/classes/weather.db");

    try (Connection conn = DriverManager.getConnection("jdbc:sqlite:" + dbPath)) {
        PreparedStatement stmt = conn.prepareStatement("SELECT * FROM users WHERE username = ? AND password = ?");
        stmt.setString(1, username);
        stmt.setString(2, password);
        ResultSet rs = stmt.executeQuery();
        if (rs.next()) {
            authenticated = true;
            String firstname = rs.getString("firstname");
            String lastname = rs.getString("lastname");

            // Create a session and store user details
            //HttpSession session = request.getSession();
            // Use the implicit session object
            session.setAttribute("username", username);
            session.setAttribute("firstname", firstname);
            session.setAttribute("lastname", lastname);
            session.setMaxInactiveInterval(2 * 60 * 60); // 2 hours

            response.sendRedirect("dashboard.jsp");
            return;
        }
    } catch (Exception e) {
        e.printStackTrace();
    }

    // Authentication failed, redirect back to login page
    response.sendRedirect("/?error=invalid");
%>