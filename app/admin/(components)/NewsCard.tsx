import { Card, Typography } from "antd";
import React from "react";

export default function NewsCard({
  title,
  image,
  description,
}: {
  title?: string;
  image?: string;
  description?: string;
}) {
  return (
    <Card
      hoverable
      bordered
      style={{
        borderRadius: 40,
        margin: "1rem",
      }}
      cover={
        <img
          style={{
            borderTopLeftRadius: 40,
            borderTopRightRadius: 40,
            width: "100%",
          }}
          alt="example"
          src="https://images.pexels.com/photos/257736/pexels-photo-257736.jpeg"
        />
      }
    >
      <Typography.Text
        strong
        style={{
          fontSize: "1rem",
          margin: "0.5rem 0",
        }}
      >
        New Development for Admin Side
      </Typography.Text>
      <Typography.Paragraph
        style={{
          fontSize: "0.8rem",
        }}
      >
        Lorem, ipsum dolor sit amet consectetur adipisicing elit. Nesciunt
        dolorem hic, deserunt provident neque delectus sequi. Perferendis
        pariatur iure nihil illo! Iure, ut possimus. Ab, commodi tempore! Alias,
        molestias harum.
      </Typography.Paragraph>
    </Card>
  );
}
