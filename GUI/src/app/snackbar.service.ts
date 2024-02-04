import { Injectable } from '@angular/core';
import { MatSnackBar, MatSnackBarConfig  } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root'
})

//This class defines the SnackbarService (PopUp Window for hint messages)
export class SnackbarService {
  constructor(private snackBar: MatSnackBar) {}

  //Function that other components call up to display the pop-up message window with the corresponding message
  showSuccess(message: string): void {
    const snackBarConfig: MatSnackBarConfig = {  
      duration: 3000,
      horizontalPosition: 'end',
      verticalPosition: 'top',
      panelClass: ['snackbar'],
    };

    this.snackBar.open(message, 'Close', snackBarConfig);
  }
}
