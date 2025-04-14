"use client";

import React from "react";
import Image from "next/image";
import logo from "@/public/img/logo.png";
import styles from "./ProfileForm.module.css";
import { FileText, GitPullRequest, Clock, Github, Slack } from "lucide-react";
import { Avatar } from "antd";
import { UserOutlined } from "@ant-design/icons";

const ProfileForm: React.FC = () => {
  return (
    <div className={styles.container}>
      {/* Header with Avatar */}
      <div className={styles.header}>
        <div className={styles.logoWrapper}>
          <Image src={logo} alt="Profile" width={150} height={50} />
        </div>
        <div className={styles.avatarSection}>
          <div className={styles.avatar}>
            <Avatar
              size={120}
              icon={<UserOutlined />}
              className={styles.avatarImage}
            />
            <button className={styles.changeAvatarBtn}>Change Photo</button>
          </div>
        </div>
        <h2>Profile Settings</h2>
        <p>Manage your account settings and profile information</p>
      </div>
      {/* Stats Cards */}
      <div className={styles.statsGrid}>
        <div className={styles.statCard}>
          <FileText size={24} />
          <div>
            <h4>Total RFPs</h4>
            <span>24</span>
          </div>
        </div>
        <div className={styles.statCard}>
          <GitPullRequest size={24} />
          <div>
            <h4>Active Proposals</h4>
            <span>8</span>
          </div>
        </div>
        <div className={styles.statCard}>
          <Clock size={24} />
          <div>
            <h4>Last Activity</h4>
            <span>2 hours ago</span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className={styles.contentGrid}>
        {/* Form Section */}
        <div className={styles.formWrapper}>
          <form className={styles.form}>
            <div className={styles.formGrid}>
              {/* Personal Information */}
              <div className={styles.formSection}>
                <h3>Personal Information</h3>
                <div className={styles.inputGroup}>
                  <label htmlFor="name">Name | Surname</label>
                  <input type="text" id="name" defaultValue="Jessica Jane" />
                </div>
                <div className={styles.inputGroup}>
                  <label htmlFor="email">E-mail</label>
                  <input
                    type="email"
                    id="email"
                    defaultValue="jessicajane000000@gmail.com"
                  />
                </div>
                <div className={styles.inputGroup}>
                  <label htmlFor="phone">Phone Number</label>
                  <input type="tel" id="phone" defaultValue="+905000000000" />
                </div>
              </div>

              {/* Company & Security */}
              <div className={styles.formSection}>
                <h3>Company & Security</h3>
                <div className={styles.inputGroup}>
                  <label htmlFor="company">Company Name</label>
                  <input
                    type="text"
                    id="company"
                    defaultValue="RFP Creator"
                    className={styles.readOnlyInput}
                    readOnly
                  />
                </div>
                <div className={styles.inputGroup}>
                  <label htmlFor="password">Change Password*</label>
                  <input
                    type="password"
                    id="password"
                    placeholder="Enter new password"
                  />
                </div>
              </div>
            </div>

            <button type="submit" className={styles.saveButton}>
              Save Changes
            </button>
          </form>
        </div>

        {/* Side Content */}
        <div className={styles.sideContent}>
          {/* Activity History */}
          <div className={styles.activitySection}>
            <h3>Recent Activity</h3>
            <div className={styles.activityList}>
              <div className={styles.activityItem}>
                <div className={styles.activityDot} />
                <p>Created new RFP: &quot;Cloud Infrastructure&quot;</p>
                <span>Today, 14:03</span>
              </div>
              <div className={styles.activityItem}>
                <div className={styles.activityDot} />
                <p>Updated profile information</p>
                <span>Yesterday, 16:45</span>
              </div>
              <div className={styles.activityItem}>
                <div className={styles.activityDot} />
                <p>Submitted proposal for &quot;Network Security&quot;</p>
                <span>2 days ago</span>
              </div>
            </div>
          </div>

          {/* Connected Accounts */}
          <div className={styles.connectedAccounts}>
            <h3>Connected Accounts</h3>
            <div className={styles.accountsList}>
              <div className={styles.accountItem}>
                <Github size={20} />
                <span>GitHub</span>
                <button className={styles.connectBtn}>Connect</button>
              </div>
              <div className={styles.accountItem}>
                <Slack size={20} />
                <span>Slack</span>
                <button className={styles.connectedBtn}>Connected</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileForm;
