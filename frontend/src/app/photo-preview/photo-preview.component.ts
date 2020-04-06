import { Component, OnInit, Input, SimpleChange } from '@angular/core';

@Component({
  selector: 'app-photo-preview',
  templateUrl: './photo-preview.component.html',
  styleUrls: ['./photo-preview.component.css']
})
export class PhotoPreviewComponent {
  public imagePath;
  @Input('imgUrl') imgURL: any;
  public message: string;
   
}
