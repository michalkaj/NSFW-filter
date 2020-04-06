import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { PhotoPreviewComponent } from './photo-preview/photo-preview.component';
import { DomSanitizer } from '@angular/platform-browser';


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
  resultPath : any;
  public isLoading: boolean;
  selectedFile: File;
  constructor(private http: HttpClient, private sanitizer: DomSanitizer) {
    this.isLoading=false;
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
      uploadData.append('image_file', this.selectedFile, this.selectedFile.name);

      var address = this.paths['server-http'] + this.paths['blur-path'];
      this.resultPath = null;
      this.isLoading=true;


      const httpOptions = {
        headers: new HttpHeaders({
          'Content-Type':  'image/jpeg',
        })
      };

      this.http.post(
        address,
        uploadData,
        { 'responseType': 'blob' }
      ).subscribe(blob => this.displayPhoto(blob));

    }

    public displayPhoto(blob) {
        let objectURL = URL.createObjectURL(blob);
        this.resultPath = this.sanitizer.bypassSecurityTrustUrl(objectURL);
        this.isLoading = false;
    }

    public getJSON(): Observable<any> {
      return this.http.get(this._jsonURL);
    }
}

