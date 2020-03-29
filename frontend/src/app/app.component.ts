import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { PhotoPreviewComponent } from './photo-preview/photo-preview.component';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  title = 'NSFW-frontend';
  private _jsonURL = 'assets/config.json';
  private paths: any = [];
  currentPath : any;
  selectedFile: File;
  constructor(private http: HttpClient) {
    this.getJSON().subscribe(data => this.paths=data, error => console.log(error));
  }
    onFileChanged(event){
    this.selectedFile = event.target.files[0]
    const reader = new FileReader();
    reader.readAsDataURL(this.selectedFile);
    reader.onload = (event) => {
      this.currentPath = reader.result;
    };
    }

    onUpload(){
      const uploadData = new FormData();
      uploadData.append('myFile', this.selectedFile, this.selectedFile.name);
      this.http.post(this.paths['server-http']+this.paths['blur-path']+"/"+this.selectedFile.name, uploadData, {
        reportProgress: true,
        observe: 'events',
      }).subscribe(event => {console.log(event);})

    }

    public getJSON(): Observable<any> {
      return this.http.get(this._jsonURL);
    }
}

