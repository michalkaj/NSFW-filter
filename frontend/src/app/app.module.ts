import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { AppComponent } from './app.component';
import {  PhotoPreviewComponent } from './photo-preview/photo-preview.component';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {FormsModule} from '@angular/forms';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import { BlurComponent } from './blur/blur.component';
import { NsfwComponent } from './nsfw/nsfw.component';
import { TestingComponent } from './testing/testing.component';
import { AppRoutingModule } from './app-routing/app-routing.module';
import { StartPageComponent } from './start-page/start-page.component';




@NgModule({
  declarations: [
    AppComponent,
    PhotoPreviewComponent,
    BlurComponent,
    NsfwComponent,
    TestingComponent,
    StartPageComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatProgressSpinnerModule,
    FormsModule,
    MatSlideToggleModule,
    AppRoutingModule,  
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
