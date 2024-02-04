import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { DialogComponent } from '../app/dialog/dialog.component';

@Injectable({
  providedIn: 'root',
})

//The class is a service that provides the DialogComponent for all other components and allows to diplay a dialog box.
export class DialogService {
  constructor(private dialog: MatDialog) {}

  //This method opens a dialog box with a given title and a message coming from the DialogCompopnete
  openDialog(title: string, message: string): void {
    this.dialog.open(DialogComponent, {
      width: '250px',
      data: { title, message },
    });
  }
}
