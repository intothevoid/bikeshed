// Backend webservice to display the status of the server.

// imports

use actix_web::{web, App, HttpResponse, HttpServer};
use serde_json;
use std::collections::HashMap;

// function to handle the /status request
async fn status() -> actix_web::Result<HttpResponse> {
    let mut status_data = HashMap::new();
    status_data.insert("status", "OK");
    let status_json = serde_json::to_string(&status_data).unwrap();
    let res = HttpResponse::Ok()
        .content_type("application/json")
        .body(status_json);

    // wrap res into Result
    Ok(res)
}

// function to handle the /start request
async fn start() -> actix_web::Result<HttpResponse> {
    let mut status_data = HashMap::new();
    status_data.insert("status", "Starting");
    let status_json = serde_json::to_string(&status_data).unwrap();
    let res = HttpResponse::Ok()
        .content_type("application/json")
        .body(status_json);

    Ok(res)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/status", web::get().to(status))
            .route("/start", web::get().to(start))
    })
    .bind("0.0.0.0:8080")?
    .run()
    .await
}
