library(shiny)
library(shinydashboard)
library(dplyr)
library(ggplot2)
library(DT)
library(lubridate)

# Initialize sample data
init_leads <- function() {
  data.frame(
    id = 1:5,
    name = c("Acme Corp", "TechStart Inc", "Local Bakery", "Design Studio", "Consulting Group"),
    email = c("contact@acme.com", "hello@techstart.com", "info@bakery.com", "hello@design.com", "team@consult.com"),
    phone = c("555-0101", "555-0102", "555-0103", "555-0104", "555-0105"),
    source = c("Google Ads", "Referral", "Website Form", "Cold Outreach", "Referral"),
    score = c(85, 72, 45, 90, 68),
    status = c("Hot", "Warm", "Cold", "Hot", "Warm"),
    last_contact = as.Date(c("2026-05-20", "2026-05-15", "2026-05-10", "2026-05-22", "2026-05-18")),
    next_followup = as.Date(c("2026-05-28", "2026-05-25", "2026-05-28", "2026-05-25", "2026-05-29")),
    notes = c("Budget approved", "Waiting on decision", "Low interest", "Ready to close", "Negotiating terms")
  )
}

# UI
ui <- dashboardPage(
  dashboardHeader(title = "Lead Tracker MVP"),

  dashboardSidebar(
    sidebarMenu(
      menuItem("Dashboard", tabName = "dashboard", icon = icon("chart-bar")),
      menuItem("All Leads", tabName = "leads", icon = icon("list")),
      menuItem("Add Lead", tabName = "add_lead", icon = icon("plus")),
      menuItem("Analytics", tabName = "analytics", icon = icon("chart-line"))
    )
  ),

  dashboardBody(
    tabItems(
      # Dashboard Tab
      tabItem(tabName = "dashboard",
        fluidRow(
          valueBoxOutput("total_leads", width = 3),
          valueBoxOutput("hot_leads", width = 3),
          valueBoxOutput("due_today", width = 3),
          valueBoxOutput("conversion_rate", width = 3)
        ),

        fluidRow(
          box(
            title = "Lead Status Distribution",
            plotOutput("status_chart"),
            width = 6
          ),
          box(
            title = "Top Lead Sources",
            plotOutput("source_chart"),
            width = 6
          )
        ),

        fluidRow(
          box(
            title = "Upcoming Follow-ups (Next 7 Days)",
            DT::dataTableOutput("upcoming_table"),
            width = 12
          )
        )
      ),

      # All Leads Tab
      tabItem(tabName = "leads",
        fluidRow(
          column(12,
            h3("Lead Database"),
            DT::dataTableOutput("all_leads_table")
          )
        )
      ),

      # Add Lead Tab
      tabItem(tabName = "add_lead",
        fluidRow(
          box(
            title = "Add New Lead",
            status = "primary",
            solidHeader = TRUE,
            width = 6,

            textInput("new_name", "Company Name*", placeholder = "Enter company name"),
            textInput("new_email", "Email*", placeholder = "contact@company.com"),
            textInput("new_phone", "Phone", placeholder = "555-0000"),

            selectInput("new_source", "Lead Source*",
              choices = c("Google Ads", "Referral", "Website Form", "Cold Outreach", "Social Media", "Event", "Other"),
              selected = "Website Form"),

            sliderInput("new_score", "Lead Score (0-100)",
              min = 0, max = 100, value = 50),

            selectInput("new_status", "Status*",
              choices = c("Cold", "Warm", "Hot"),
              selected = "Warm"),

            textAreaInput("new_notes", "Notes",
              placeholder = "Any relevant notes about this lead...", rows = 3),

            actionButton("submit_lead", "Add Lead", class = "btn-success"),
            actionButton("clear_form", "Clear", class = "btn-secondary")
          ),

          box(
            title = "Success!",
            status = "success",
            width = 6,
            htmlOutput("success_message"),
            p("✓ Quick follow-up tasks:"),
            tags$ul(
              tags$li("Send welcome email to new lead"),
              tags$li("Set a reminder for 48-hour follow-up"),
              tags$li("Add to your CRM if you have one")
            )
          )
        )
      ),

      # Analytics Tab
      tabItem(tabName = "analytics",
        fluidRow(
          box(
            title = "Lead Score Distribution",
            plotOutput("score_distribution"),
            width = 6
          ),
          box(
            title = "Conversion Metrics",
            htmlOutput("conversion_metrics"),
            width = 6
          )
        ),

        fluidRow(
          box(
            title = "Lead Age Analysis",
            plotOutput("age_analysis"),
            width = 12
          )
        )
      )
    )
  )
)

# Server
server <- function(input, output, session) {

  # Reactive values
  leads_data <- reactiveVal(init_leads())

  # Dashboard - Value Boxes
  output$total_leads <- renderValueBox({
    valueBox(
      nrow(leads_data()),
      "Total Leads",
      icon = icon("users"),
      color = "blue"
    )
  })

  output$hot_leads <- renderValueBox({
    hot_count <- nrow(filter(leads_data(), status == "Hot"))
    valueBox(
      hot_count,
      "Hot Leads",
      icon = icon("fire"),
      color = "red"
    )
  })

  output$due_today <- renderValueBox({
    today <- Sys.Date()
    due <- nrow(filter(leads_data(), next_followup <= today))
    valueBox(
      due,
      "Due Today",
      icon = icon("clock"),
      color = "orange"
    )
  })

  output$conversion_rate <- renderValueBox({
    hot <- nrow(filter(leads_data(), status == "Hot"))
    total <- nrow(leads_data())
    rate <- if(total > 0) round((hot / total) * 100, 1) else 0
    valueBox(
      paste0(rate, "%"),
      "Hot Lead Rate",
      icon = icon("target"),
      color = "green"
    )
  })

  # Dashboard Charts
  output$status_chart <- renderPlot({
    leads_data() %>%
      group_by(status) %>%
      summarise(count = n(), .groups = 'drop') %>%
      ggplot(aes(x = reorder(status, -count), y = count, fill = status)) +
      geom_bar(stat = "identity") +
      scale_fill_manual(values = c("Hot" = "#FF6B6B", "Warm" = "#FFA500", "Cold" = "#4ECDC4")) +
      labs(title = "Leads by Status", x = "Status", y = "Count") +
      theme_minimal() +
      theme(legend.position = "none")
  })

  output$source_chart <- renderPlot({
    leads_data() %>%
      group_by(source) %>%
      summarise(count = n(), .groups = 'drop') %>%
      arrange(desc(count)) %>%
      head(8) %>%
      ggplot(aes(x = reorder(source, count), y = count, fill = source)) +
      geom_bar(stat = "identity") +
      coord_flip() +
      labs(title = "Leads by Source", x = "", y = "Count") +
      theme_minimal() +
      theme(legend.position = "none")
  })

  # Upcoming follow-ups
  output$upcoming_table <- DT::renderDataTable({
    today <- Sys.Date()
    leads_data() %>%
      filter(next_followup >= today & next_followup <= today + 7) %>%
      select(name, email, phone, status, next_followup, notes) %>%
      arrange(next_followup) %>%
      datatable(options = list(pageLength = 10, autoWidth = TRUE))
  })

  # All leads table
  output$all_leads_table <- DT::renderDataTable({
    leads_data() %>%
      select(name, email, phone, source, score, status, last_contact, next_followup) %>%
      datatable(options = list(pageLength = 20, autoWidth = TRUE))
  })

  # Add lead functionality
  observeEvent(input$submit_lead, {
    if(input$new_name == "" || input$new_email == "") {
      showNotification("Please fill in all required fields", type = "error")
      return()
    }

    new_lead <- data.frame(
      id = max(leads_data()$id) + 1,
      name = input$new_name,
      email = input$new_email,
      phone = input$new_phone,
      source = input$new_source,
      score = input$new_score,
      status = input$new_status,
      last_contact = Sys.Date(),
      next_followup = Sys.Date() + 2,
      notes = input$new_notes
    )

    leads_data(rbind(leads_data(), new_lead))

    # Clear form
    updateTextInput(session, "new_name", value = "")
    updateTextInput(session, "new_email", value = "")
    updateTextInput(session, "new_phone", value = "")
    updateSliderInput(session, "new_score", value = 50)
    updateSelectInput(session, "new_status", selected = "Warm")
    updateTextAreaInput(session, "new_notes", value = "")

    showNotification(paste("Lead added:", input$new_name), type = "message")
  })

  observeEvent(input$clear_form, {
    updateTextInput(session, "new_name", value = "")
    updateTextInput(session, "new_email", value = "")
    updateTextInput(session, "new_phone", value = "")
    updateSliderInput(session, "new_score", value = 50)
    updateTextAreaInput(session, "new_notes", value = "")
  })

  output$success_message <- renderUI({
    HTML("<p style='color: green; font-size: 18px;'><strong>✓ Lead Added Successfully!</strong></p>")
  })

  # Analytics Charts
  output$score_distribution <- renderPlot({
    leads_data() %>%
      ggplot(aes(x = score, fill = status)) +
      geom_histogram(binwidth = 10, alpha = 0.7) +
      scale_fill_manual(values = c("Hot" = "#FF6B6B", "Warm" = "#FFA500", "Cold" = "#4ECDC4")) +
      labs(title = "Lead Score Distribution", x = "Score", y = "Count") +
      theme_minimal()
  })

  output$conversion_metrics <- renderUI({
    total <- nrow(leads_data())
    hot <- nrow(filter(leads_data(), status == "Hot"))
    warm <- nrow(filter(leads_data(), status == "Warm"))
    cold <- nrow(filter(leads_data(), status == "Cold"))
    avg_score <- round(mean(leads_data()$score), 1)

    HTML(paste(
      "<p><strong>Total Leads:</strong>", total, "</p>",
      "<p><strong>Hot Leads:</strong>", hot, "(",
      round((hot/total)*100, 1), "%)", "</p>",
      "<p><strong>Warm Leads:</strong>", warm, "(",
      round((warm/total)*100, 1), "%)", "</p>",
      "<p><strong>Cold Leads:</strong>", cold, "(",
      round((cold/total)*100, 1), "%)", "</p>",
      "<hr>",
      "<p><strong>Average Lead Score:</strong>", avg_score, "</p>"
    ))
  })

  output$age_analysis <- renderPlot({
    leads_data() %>%
      mutate(days_since = as.numeric(Sys.Date() - last_contact)) %>%
      ggplot(aes(x = days_since, y = score, color = status, size = score)) +
      geom_point(alpha = 0.6) +
      scale_color_manual(values = c("Hot" = "#FF6B6B", "Warm" = "#FFA500", "Cold" = "#4ECDC4")) +
      labs(title = "Lead Age vs Quality",
           x = "Days Since Last Contact",
           y = "Lead Score",
           subtitle = "Larger bubbles = higher quality leads") +
      theme_minimal()
  })
}

# Run the app
shinyApp(ui, server)
