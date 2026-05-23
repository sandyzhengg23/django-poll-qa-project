import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "30s", target: 5 },
    { duration: "1m", target: 10 },
    { duration: "30s", target: 0 },
  ],
  thresholds: {
    http_req_failed: ["rate<0.05"],
    http_req_duration: ["p(95)<800"],
  },
  summaryTrendStats: ["avg", "min", "med", "p(90)", "p(95)", "p(99)", "max"],
};

const BASE_URL = "http://127.0.0.1:8000";

export default function () {
  let home = http.get(`${BASE_URL}/`);
  check(home, {
    "home page status is 200": (r) => r.status === 200,
  });

  let login = http.get(`${BASE_URL}/accounts/login/`);
  check(login, {
    "login page status is 200": (r) => r.status === 200,
  });

  let register = http.get(`${BASE_URL}/accounts/register/`);
  check(register, {
    "register page status is 200": (r) => r.status === 200,
  });

  sleep(1);
}