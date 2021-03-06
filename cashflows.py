from pylab import *

class Cashflow:
    # # Prepayment Rate (CPR)
    # rmbs_cpr = 0.050

    # # Mortgage Type (1 == Fixed Principal)
    # cb_mortgage_type = 0

    # # MBS Outstanding Balance
    # outstanding_balance = 100000

    # # MBS Average Period
    # term = 360

    # # MBS Average Rate
    # mortgage_rate = 0.16

    # # MBS Senior Tranche Balance
    # senior_req = 50000

    # # MBS Senior Tranche Rate
    # senior_rate = 0.03

    # # MBS Junior Tranche Balance
    # junior_req = 10000

    # # MBS Junior Tranche Rate
    # junior_rate = 0.11 ## junior rate

    # # Tranches
    # mortgage_cf = []
    # senior_cf = []
    # junior_cf = []
    # equity_cf = []

    def __init__(self, rmbs_cpr = 0.050, cb_mortgage_type = 0, outstanding_balance = 100000, term = 360, mortgage_rate = 0.16, senior_req = 50000, senior_rate = 0.03, junior_req = 10000, junior_rate = 0.11):
        self.rmbs_cpr = float(rmbs_cpr)
        self.cb_mortgage_type = float(cb_mortgage_type)
        self.outstanding_balance = float(outstanding_balance)
        self.term = int(term)
        self.mortgage_rate = float(mortgage_rate)
        self.senior_req = float(senior_req)
        self.senior_rate = float(senior_rate)
        self.junior_req = float(junior_req)
        self.junior_rate = float(junior_rate)
        self.mortgage_cf = []
        self.senior_cf = []
        self.junior_cf = []
        self.equity_cf = []

    ## 1 == fixed principal
    def cal_rmbs(self):
        # calculate the SMM based on assumed CPR
        smm = 1 - math.pow( 1 - self.rmbs_cpr, 1/12.0)
        # print smm
        # print "SMM %f" % smm
        balance = self.outstanding_balance
        # print balance
        period = self.term
        # mortgage_rate =

        r = self.mortgage_rate / 12.0
        # print self.rmbs_mortgageType.get()
        if self.cb_mortgage_type == 1 :
        # fix principal method
            monthly_principal = balance / period
            for i in range(period):
                mcf = 0.0
                mcf += monthly_principal
                mcf += balance * r
                mcf += balance * smm
                if balance >= monthly_principal:
                    balance -= monthly_principal
                else:
                    break
                if balance >= balance * smm:
                    balance -= balance * smm
                else:
                    break
                self.mortgage_cf.append(mcf)
        #fix amount method
        else:
            mthpyt = balance * r * math.pow((1 + r),period) / (math.pow((1 + r),period) -1)
            for i in range(period):
                mcf = 0.0
                interest = balance * r
                mcf += mthpyt
                mcf += balance * smm

                if balance >= (mthpyt - interest):
                    balance -= mthpyt - interest
                else:
                    break
                if balance >= balance * smm:
                    balance -= balance * smm
                else:
                    break

                self.mortgage_cf.append(mcf)

        # self.mortgage_cf = x for x in self.mortgage_cf if x > 0

        self.senior_req = self.senior_req * self.senior_rate
        self.junior_req = self.junior_req * self.junior_rate

        # this is the waterfall
        for i in self.mortgage_cf:
            if i <= self.senior_req:
                # if we have less than the senior requirement then only the senior tranche is paid
                self.senior_cf.append(i)
                self.junior_cf.append(0)
                self.equity_cf.append(0)
            elif i <=  self.senior_req + self.junior_req:
                # append the full senior requirement to the tranche
                # and give the remainder to the senior, equity tranche gets nothing
                self.senior_cf.append(self.senior_req)
                self.junior_cf.append(i - self.senior_req)
                self.equity_cf.append(0)
            else:
                # if monthly cashflows are sufficient then all tranches get paid
                self.senior_cf.append(self.senior_req)
                self.junior_cf.append(self.junior_req)
                self.equity_cf.append(i - self.senior_req - self.junior_req)

        self.rmbs_render()


    def rmbs_render(self):
        plt.cla()
        x = np.arange(0.0, len(self.mortgage_cf), 1)

        plot(x, self.mortgage_cf,color = '#ff9999',linewidth = 2.0, label = 'Total MBS Cash Flow')
        plot(x, self.equity_cf,color = '#BB1BF5',linewidth = 2.0, label = 'Equity Tranche Cash Flow')
        plot(x, self.junior_cf,color = '#2340E8',linewidth = 2.0, label = 'Junior Tranche Cash Flow')
        plot(x, self.senior_cf,color = '#1DF0A2',linewidth = 2.0, label = 'Senior Tranche Cash Flow')

        legend( ('Total MBS Cash Flow', 'Equity Tranche Cash Flow', 'Junior Tranche Cash Flow','Senior Tranche Cash Flow'), loc='upper right')
        plt.grid(True)
        plt.show()