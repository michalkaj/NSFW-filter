import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TestingComponent } from '../testing/testing.component'
import {BlurComponent} from '../blur/blur.component'
import {StartPageComponent} from '../start-page/start-page.component'
import {NsfwComponent} from '../nsfw/nsfw.component'


const routes: Routes = [
    {
        path: '',
        component: StartPageComponent,

    },
    {
        path: 'testing',
        component: TestingComponent,

    },
    {
        path: 'blur',
        component: BlurComponent,

    },
    {
        path: 'nsfw',
        component: NsfwComponent,

    },
    {
        path:'**',
        redirectTo: '',
    }
    
];

@NgModule({
    imports: [
        RouterModule.forRoot(routes)
    ],
    exports: [
        RouterModule
    ],
    declarations: []
})
export class AppRoutingModule { }
