""" 
    @worker.task(task_type="contractReminder")
    async def contract_reminder(job: Job):
        print("Contract reminder send")

    @worker.task(task_type="checkContractAnswer")
    async def check_contract_answer(job: Job):
        print("Contract answer checked")

    @worker.task(task_type="cancelContractNegotiation")
    async def cancel_contract_negotiation(job: Job):
        print("Contract Negotiation cancelled")

    @worker.task(task_type="sendAdjustedContract")
    async def send_adjusted_contract(job: Job):
        print("Adjusted Contract send")

    @worker.task(task_type="saveContract")
    async def save_contract(job: Job):
        print("Contract saved")
        
    @worker.task(task_type="checkTopCandidatesAmount")
    async def checkTopCandidatesAmount(job: Job):
        print("Top Candidates Amount")

    @worker.task(task_type="sendJobStandards")
    async def send_job_standards(job: Job):
        print("Job standards send")

    @worker.task(task_type="sendReminderForConfirmation")
    async def send_reminder_for_confirmation(job: Job):
        print("Reminder for confirmation send")

    @worker.task(task_type="cancelContract")
    async def cancel_contract(job: Job):
        print("Contract cancelled")

    @worker.task(task_type="inquireCandidateSearchProgress")
    async def inquire_candidate_search_process(job: Job):
        print("Inquiry candidate search progress send")

    @worker.task(task_type="storeAndSortCandidates")
    async def store_and_sort_candidates(job: Job):
        print("Candidates stored and sorted")

    @worker.task(task_type="checkingEmployedCandidates")
    async def checking_employed_candidates(job: Job):
        print("Employed candidates checked")

    @worker.task(task_type="sendWeplacmInfoEmployed")
    async def send_weplacm_info_employed(job: Job):
        print("WEPLACM Info about employed candidates send")

    @worker.task(task_type="checkInvoice")
    async def check_invoice(job: Job):
        print("Invoice checked")

    @worker.task(task_type="sendWeplacmInfoWrongInvoice")
    async def send_weplacm_info_wrong_invoice(job: Job):
        print("Info about wrong invoice send")

    @worker.task(task_type="payInvoice")
    async def pay_invoice(job: Job):
        print("Invoice paid")

    @worker.task(task_type="moveCandidatesToTopDatabase")
    async def moce_candidates_to_topdatabase(job: Job):
        print("Candidates moved to TopDatabase")

    @worker.task(task_type="rejectionMailToCandidate")
    async def rejection_mail_to_candidate(job: Job):
        print("Rejection Mail send to candidate")

    @worker.task(task_type="removeCandidateFromDatabase")
    async def remove_candidate_from_database(job: Job):
        print("Candidate removed from Database")

    @worker.task(task_type="checkEntrysInCandidateDB")
    async def check_entrys_in_candidatedb(job: Job):
        print("Entry's checked in CandidateDB")

    @worker.task(task_type="MoreRequest")
    async def more_request(job: Job):
        print("Requested more candidates")

    @worker.task(task_type="scheduleInterviewDates")
    async def schedule_interview_dates(job: Job):
        print("Interview dates scheduled")

    @worker.task(task_type="checkInterviewerAnswer")
    async def check_interviewer_answer(job: Job):
        print("Interviewer answer checked")

    @worker.task(task_type="informPeopleInvolved")
    async def inform_people_involved(job: Job):
        print("People involved are informed")

    @worker.task(task_type="bookSuitableRoom")
    async def book_suitable_room(job: Job):
        print("Suitable room booked")

    @worker.task(task_type="sendCandidateInterviewDate")
    async def send_candidate_interview_date(job: Job):
        print("Interview date send to candidate")

    @worker.task(task_type="cancelInterviewWithCandidate")
    async def cancel_interview_with_candidate(job: Job):
        print("Interview with candidate cancelled")

    @worker.task(task_type="sendReminderToCandidate")
    async def send_reminder_to_candidate(job: Job):
        print("Reminder send toi candidate")

    @worker.task(task_type="checkCandidateAnswer")
    async def check_candidate_answer(job: Job):
        print("Candidate answer checked")

    @worker.task(task_type="deleteRoomBooking")
    async def delete_room_booking(job: Job):
        print("Booking deleted")

    @worker.task(task_type="saveInterviewDate")
    async def save_interview_date(job: Job):
        print("Interview date saved")

    @worker.task(task_type="cancelInterviewDateWithInterviewers")
    async def cancel_interview_date_with_interviewers(job: Job):
        print("Interview cancelled with interviewers")

    @worker.task(task_type="calculatedCandidateEvaluation")
    async def calculate_candidate_evaluation(job: Job):
        print("Calculation of candidate evaluation done")

    @worker.task(task_type="sendConfirmationAndContractToCandidate")
    async def send_confirmation_and_contract_to_candidate(job: Job):
        print("Confirmation and contract send to candidate")

    @worker.task(task_type="analyseCandidateResponse")
    async def analyse_candidate_response(job: Job):
        print("Candidates response analysed")

    @worker.task(task_type="moveCandidateToSystemDB")
    async def move_candidate_to_systemdb(job: Job):
        print("Candidate moved to sytsemDB")

    @worker.task(task_type="checkScheduledInterviews")
    async def check_scheduled_interviews(job: Job):
        print("Scheduled interviews checked")

    @worker.task(task_type="cancelAllInterviews")
    async def cancel_all_interviews(job: Job):
        print("All interviews cancelled")

    @worker.task(task_type="removeAllCandidatesFromDB")
    async def remove_all_candidates_from_db(job: Job):
        print("All candidates from databases removed")

    @worker.task(task_type="answerInquiryFromWeplacm")
    async def inquiry_from_weplacm(job: Job):
        print("Inquiry from WEPLACM answered")
        
    @worker.task(task_type="scheduleInterviewDate")
    async def inquiry_from_weplacm(job: Job):
        print("Interview scheduled")
         """