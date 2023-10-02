import { Component } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Component({
  selector: "app-main-card",
  templateUrl: "./main-card.component.html",
  styleUrls: ["./main-card.component.css"],
})
export class MainCardComponent {
  inputText: string = "";
  displayForText: any[] = [];
  displayAgainstText: any[] = [];
  isLoading = false;
  negatedSentence: string = "";
  constructor(private http: HttpClient) {}


  sendRequest() {
    console.log(this.inputText);
    this.isLoading = true;
    this.displayAgainstText = [];
    this.displayForText = [];
    const url = "/submit?query=" + encodeURIComponent(this.inputText);
    this.http.get(url).subscribe((response) => {
      console.log(response);
      let responseJSON = Object.values(response);
      this.displayAgainstText = responseJSON[0];
      this.displayForText = responseJSON[1];
      this.negatedSentence = responseJSON[2];
      this.isLoading = false;
    });
  }
}
